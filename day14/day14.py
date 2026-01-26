import os.path
from timeit import default_timer as timer


def part1(data: list[str]) -> int:
    mask_0, mask_1 = 0, 0
    mem: dict[int, int] = {}

    for line in data:
        op, value = line.split(" = ")
        if op == "mask":
            mask_0 = ~ sum(2**i for i, c in enumerate(reversed(value)) if c == "0")  # 1's complement
            mask_1 = sum(2**i for i, c in enumerate(reversed(value)) if c == "1")
        else:
            address, val = int(op[4:-1]), int(value)
            mem[address] = val & mask_0 | mask_1

    return sum(mem.values())


def part2(data: list[str]) -> int:
    mask_1 = 0
    mask_floating = []
    mem: dict[int, int] = {}

    def floating(idx: int, address: int, val: int) -> None:
        nonlocal mem, mask_floating
        if idx == len(mask_floating):
            return
        add_0 = address & ~mask_floating[idx]
        add_1 = address | mask_floating[idx]
        mem[add_0] = val
        mem[add_1] = val
        floating(idx+1, add_0, val)
        floating(idx+1, add_1, val)

    for line in data:
        op, value = line.split(" = ")
        if op == "mask":
            mask_1 = sum(2**i for i, c in enumerate(reversed(value)) if c == "1")
            mask_floating = [2**i for i, c in enumerate(reversed(value)) if c == "X"]
        else:
            address, val = int(op[4:-1]), int(value)
            address |= mask_1
            floating(0, address, val)
    return sum(mem.values())


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()


print("Part 1:", part1(data))
print("Part 2:", part2(data))

e = timer()
print("time:", e - s)
