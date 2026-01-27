import os.path
from timeit import default_timer as timer
import numpy as np
from scipy.ndimage import convolve


def solve(grid: np.ndarray, N: int, cycles: int) -> int:
    # make the grid N dimensional
    for _ in range(N-2):
        grid = np.expand_dims(grid, -1)

    # 3^N-1 neighbor kernel
    # 26 for 3D
    # 80 for 4D
    kernel = np.ones((3,)*N)
    kernel[(1,)*N] = 0

    return conway(grid, kernel, cycles)


def conway(grid: np.ndarray, kernel: np.ndarray, cycles: int) -> int:
    for _ in range(cycles):
        # pad every cycle by 1
        grid = np.pad(grid, 1)

        # count active neighbors
        neighbors = convolve(grid, kernel, mode="constant")

        # deactivate rule
        grid[(neighbors < 2) | (neighbors > 3)] = 0

        # activate rule
        grid[(neighbors == 3)] = 1

        # both rules, not faster
        # grid = np.where((neighbors == 3) | (grid & (neighbors == 2)), 1, 0)
    return grid.sum()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()


# convert input to 2D grid
converter = str.maketrans('.#', '01')
grid = np.array([[int(x) for x in row.translate(converter)] for row in data])

print("Part 1:", solve(grid, 3, 6))
print("Part 2:", solve(grid, 4, 6))


e = timer()
print("time:", e - s)
