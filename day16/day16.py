import os.path
from timeit import default_timer as timer


# return ordered union of ranges r1 and r2
def union_ranges(r1: range, r2: range) -> list[range]:

    # disjoint?
    if r1.stop < r2.start:
        return [r1, r2]
    elif r2.stop < r1.start:
        return [r2, r1]

    return [range(min(r1.start, r2.start), max(r1.stop, r2.stop))]


# update ordered list of disjoint ranges with a new range
def update_ranges(ranges: list[range], new_range: range) -> list[range]:
    if len(ranges) == 0:
        return [new_range]
    if new_range.stop < ranges[0].start:
        return [new_range] + ranges
    if new_range.start > ranges[-1].stop:
        return ranges + [new_range]

    idx = 0
    for idx in range(len(ranges)):
        if ranges[idx].stop >= new_range.start:
            break

    new_ranges = ranges[:idx+1]
    left = new_ranges.pop()
    right = new_range
    while True:
        new_ranges += union_ranges(left, right)
        idx += 1
        if idx == len(ranges):
            break
        if new_ranges[-1].stop < ranges[idx].start:
            break
        left = new_ranges.pop()
        right = ranges[idx]

    new_ranges += ranges[idx:]

    return new_ranges


def create_ranges(data: str) -> list[range]:
    ranges = []
    for line in data.splitlines():
        _, ranges_str = line.split(": ")
        for range_str in ranges_str.split(" or "):
            start, stop = range_str.split("-")
            new_range = range(int(start), int(stop)+1)
            ranges = update_ranges(ranges, new_range)
    return ranges


def error_rate(ranges: list[range], data: str) -> int:
    res = 0
    for line in data.splitlines()[1:]:
        for num in map(int, line.split(",")):
            if any(num in r for r in ranges):
                continue
            else:  # invalid
                res += num
    return res


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


valid, my_ticket, nearby = data.split("\n\n")
ranges = create_ranges(valid)
p1 = error_rate(ranges, nearby)
print("Part 1:", p1)

e = timer()
print("time:", e - s)
