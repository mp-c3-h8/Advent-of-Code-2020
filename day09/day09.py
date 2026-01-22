import os.path
from timeit import default_timer as timer


def part1(numbers: list[int], preamble: int) -> tuple[int, int]:

    def is_sum(idx: int) -> bool:
        nonlocal preamble, numbers
        seen: set[int] = set()
        for j in range(idx-preamble, idx):
            if numbers[idx] - numbers[j] in seen:
                return True
            else:
                seen.add(numbers[j])
        return False

    for i in range(preamble, len(numbers)):
        if not is_sum(i):
            return i, numbers[i]

    raise ValueError("No weakness found")


def part2(numbers: list[int], target: int, target_idx: int) -> int:
    # 2 pointer approch
    # first pass to find initial interval [idx_left,...,idx_right]
    idx_left = 0
    s = 0
    for idx_right in range(0, len(numbers)):
        s += numbers[idx_right]
        if s >= target:
            break
    else:
        raise ValueError("Target sum not found")

    # gradualley increment left index
    for idx_left in range(1, target_idx):
        # are we done?
        if s == target:
            break

        s -= numbers[idx_left-1]

        # sum too big, decrease right index
        if s > target:
            for idx_right in range(idx_right, idx_left, -1):
                if s <= target:
                    break
                s -= numbers[idx_right]
        # sum too small, increase right index
        elif s < target:
            for idx_right in range(idx_right+1, len(numbers)):
                s += numbers[idx_right]
                if s >= target:
                    break
    else:
        raise ValueError("Target sum not found")

    region = sorted(numbers[idx_left-1:idx_right+1])
    return region[0] + region[-1]


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

numbers = [int(line) for line in data.splitlines()]

idx, num = part1(numbers, 25)
print("Part 1:", num)
print("Part 2:", part2(numbers, num, idx))


e = timer()
print("time:", e - s)
