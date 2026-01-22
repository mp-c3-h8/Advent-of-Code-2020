import os.path
from itertools import pairwise


def halve(left: int, right: int, take_left: bool) -> tuple[int, int]:
    half = (left+right) // 2
    if take_left:
        return left, half
    else:
        return half+1, right


def bisect(seq: str, left_char: str) -> int:
    left, right = 0, 2**len(seq)-1
    for c in seq:
        left, right = halve(left, right, c == left_char)
    return left


def seat_id(boarding_pass: str) -> int:
    row = bisect(boarding_pass[:7], "F")
    col = bisect(boarding_pass[7:], "L")
    return row*8+col


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

all_seats = sorted([seat_id(row) for row in data])
low, high = all_seats[0], all_seats[-1]
print("Part 1:",  high)

# little gauss
p2 = (high*(high+1) - low*(low-1))//2 - sum(all_seats)
print("Part 2:", p2)

for a, b in pairwise(all_seats):
    if b-a != 1:
        print("Part 2:", a+1)
        break
