import os.path
from timeit import default_timer as timer
import re
import numpy as np
from scipy.ndimage import convolve

type Tile = tuple[int, int]  # (x,y)
type Dir = tuple[int, int]  # (x,y)

# https://en.wikipedia.org/wiki/Hexagon
# chose D = 4 (for a sketch)
# scale x-axis: x -> 1/sqrt(3)*x
# scale y-axis: y -> 1/3 *y
# now neighbors are sitting on an integer grid
DIRS: dict[str, Dir] = {
    "e": (2, 0),
    "se": (1, -1),
    "sw": (-1, -1),
    "w": (-2, 0),
    "nw": (-1, 1),
    "ne": (1, 1)
}

# seems these are called "Doubled coordinates"
# see https://www.redblobgames.com/grids/hexagons/#neighbors-doubled


def flip_tiles(data: str) -> set[Tile]:
    black: set[Tile] = set()
    regex = re.compile(r"se|sw|nw|ne|e|w")
    for line in data.splitlines():
        tile: Tile = (0, 0)
        for d_str in regex.findall(line):
            d = DIRS[d_str]
            tile = (tile[0] + d[0], tile[1] + d[1])
        if tile in black:
            black.remove(tile)
        else:
            black.add(tile)
    return black


def conway(black: set[Tile], num_days: int = 100) -> set[Tile]:
    dirs = DIRS.values()
    for _ in range(num_days):
        new_black: set[Tile] = set()
        white: set[Tile] = set()
        for tile in black:
            num_black_neighbors = 0
            for d in dirs:
                n = (tile[0]+d[0], tile[1]+d[1])
                if n in black:
                    num_black_neighbors += 1
                else:
                    white.add(n)
            if num_black_neighbors in (1, 2):
                new_black.add(tile)

        for tile in white:
            if sum((tile[0]+d[0], tile[1]+d[1]) in black for d in dirs) == 2:
                new_black.add(tile)

        black = new_black

    return black


def conway_convolve(black: set[Tile], num_days: int = 100) -> int:
    x, y = map(sorted, zip(*black))
    x_min, x_max, y_min, y_max = x[0], x[-1], y[0], y[-1]
    dimx, dimy = x_max-x_min+1, y_max-y_min+1
    tiles = np.zeros((dimy, dimx), dtype=int)

    for tile in black:
        tiles[tile[1]-y_min, tile[0]-x_min] = 1

    kernel = np.array([
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0]
    ])

    # holes (non existing hexagons) dont matter
    # they start white and never turn black
    for _ in range(num_days):
        tiles = np.pad(tiles, 1)
        neighbors = convolve(tiles, kernel, int, mode="constant")
        tiles[(neighbors == 0) | (neighbors > 2)] = 0
        tiles[(neighbors == 2)] = 1

    return tiles.sum()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

black = flip_tiles(data)
print("Part 1:", len(black))


s = timer()
p2 = conway_convolve(black, 100)
e = timer()
print(f"Part 2 (convolve): {p2} (time: {e-s})")


s = timer()
black = conway(black, 100)
e = timer()
print(f"Part 2 (sets): {len(black)} (time: {e-s})")
