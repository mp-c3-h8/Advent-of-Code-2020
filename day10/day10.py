import os.path
from timeit import default_timer as timer
from collections import Counter
from functools import cache
from itertools import pairwise


def part1(joltages: list[int]) -> int:
    # joltages must be sorted
    diffs = Counter(j2-j1 for j1, j2 in pairwise(joltages))
    return diffs[1] * diffs[3]


def part2(joltages: list[int]) -> int:
    # joltages must be sorted

    @cache
    def f(idx: int) -> int:
        nonlocal joltages
        if idx == len(joltages)-1:
            return 1
        return sum(f(j) for j in (idx+1, idx+2, idx+3) if j <= len(joltages)-1 and joltages[j]-joltages[idx] <= 3)

    return f(0)


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

joltages = sorted(int(line) for line in data.splitlines())
joltages = [0] + joltages + [joltages[-1]+3]  # extend with outlet/inlet

print("Part 1:", part1(joltages))
print("Part 2:", part2(joltages))

e = timer()
print("time:", e - s)
