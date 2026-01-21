import os.path
from math import prod

type Pos = tuple[int, int]  # (y,x)


def count_trees(grid: set[Pos], dimy: int, dimx: int, dy: int, dx: int) -> int:
    res = 0
    pos: Pos = (0, 0)
    while pos[0] <= dimy:
        if pos in grid:
            res += 1
        pos = (pos[0]+dy, (pos[1] + dx) % dimx)
    return res


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

grid: set[Pos] = {(y, x) for y, row in enumerate(data) for x, c in enumerate(row) if c == "#"}
dimy, dimx = len(data), len(data[0])

print("Part 1:", count_trees(grid, dimy, dimx, 1, 3))

p2 = prod(count_trees(grid, dimy, dimx, dy, dx) for dy, dx in ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1)))
print("Part 2:", p2)
