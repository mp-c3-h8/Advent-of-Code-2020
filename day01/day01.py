import os.path
from math import prod


def part1(data: list[str]) -> int:
    seen: set[int] = set()
    for num in map(int, data):
        if 2020 - num in seen:
            return (2020-num) * num
        else:
            seen.add(num)
    raise ValueError("Does not compute")


def part2(data: list[str]) -> int:
    seen: set[int] = set()
    two_sum: dict[int, tuple[int, int]] = {}
    for num in map(int, data):
        if 2020 - num in two_sum:
            return prod(two_sum[2020 - num]) * num
        else:
            for s in seen:
                two_sum[s+num] = (s, num)
            seen.add(num)

    raise ValueError("Does not compute")


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()


print("Part 1:", part1(data))
print("Part 2:", part2(data))
