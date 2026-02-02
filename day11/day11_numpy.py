import os.path
from timeit import default_timer as timer
import numpy as np
from scipy.ndimage import convolve

'''
part 2 adapted from: https://www.reddit.com/r/adventofcode/comments/kaw6oz/comment/gfwxivh/
https://github.com/metinsuloglu/AdventofCode20/blob/main/day11.py

'''

type Grid = np.ndarray
DIRS8 = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]


def part1(grid: Grid) -> int:
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0

    for _ in range(10**6):
        old_grid = grid.copy()
        occupied_neighbors = convolve(np.where(grid == 2, 1, 0), kernel, int, mode='constant')
        grid[(grid == 1) & (occupied_neighbors == 0)] = 2
        grid[(grid == 2) & (occupied_neighbors >= 4)] = 1
        if (old_grid == grid).all():
            break
    else:
        raise ValueError("Max iterations reached.")

    return (grid == 2).sum()


def part2(grid: Grid) -> int:
    def closest_seat_coord(coord, offset):
        curr_loc = (coord[0] + offset[0], coord[1] + offset[1])
        while 0 <= curr_loc[0] < len(grid) and 0 <= curr_loc[1] < len(grid[curr_loc[0]]) and grid[curr_loc] == 0:
            curr_loc = (curr_loc[0] + offset[0], curr_loc[1] + offset[1])
        return curr_loc

    neighbors = np.array([[[closest_seat_coord((x, y), d) for d in DIRS8]
                         for y, c in enumerate(row)] for x, row in enumerate(grid)])
    neighbours = np.rollaxis(neighbors + 1, 3)

    for _ in range(10**6):
        old_grid = grid.copy()
        padded = np.pad(grid, 1)
        neighbor_vals = np.take(padded, np.ravel_multi_index(neighbours, padded.shape))
        occupied_neighbors = np.sum(neighbor_vals == 2, axis=2)

        grid[(grid == 1) & (occupied_neighbors == 0)] = 2
        grid[(grid == 2) & (occupied_neighbors >= 5)] = 1
        if (old_grid == grid).all():
            break
    else:
        raise ValueError("Max iterations reached.")
    return (grid == 2).sum()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

# 0 = no seat, 1 = empty, 2 = occupied
converter = str.maketrans('.L#', '012')
grid: Grid = np.array([[int(x) for x in row.translate(converter)] for row in data])
print("Part 1:", part1(grid.copy()))
print("Part 2:", part2(grid))

e = timer()
print("time:", e - s)
