import os.path
from timeit import default_timer as timer
import numpy as np
from typing import Iterator
from collections import defaultdict, Counter
from math import prod
from itertools import product
from scipy.ndimage import convolve

type Pos = complex  # y = 1j downwards
type Dir = complex
type Grid = dict[Pos, Tile | None]
type Edge = np.ndarray
type EdgeTuple = tuple[int, ...]

DIRS: dict[str, Dir] = {"N": -1j, "E": 1, "S": 1j, "W": -1}


class Tile:
    def __init__(self, idx: int, matrix: np.ndarray) -> None:
        self.idx = idx
        self.matrix = matrix

    # https://en.wikipedia.org/wiki/Dihedral_group_of_order_8
    def transform(self) -> Iterator[None]:
        for _ in range(2):
            for _ in range(4):
                yield None
                self.matrix = np.rot90(self.matrix)
            self.matrix = np.fliplr(self.matrix)

    # get specific edge
    def get_edge(self, d: Dir) -> Edge:
        match d:
            case -1j: return self.matrix[0, :]   # N
            case   1: return self.matrix[:, -1]  # E
            case  1j: return self.matrix[-1, :]  # S
            case -1: return self.matrix[:, 0]    # W
        raise ValueError(f"Direction {d} not defined")

    # [north_edge,west_edge]
    def get_north_and_west_edges(self) -> tuple[Edge, Edge]:
        return (self.get_edge(DIRS["N"]), self.get_edge(DIRS["W"]))

    # all 8 different edges with respect to rotations/flips
    def all_symmetry_edges(self) -> Iterator[Edge]:
        for d in ((0, ...), (..., 0), (-1, ...), (..., -1)):
            edge = self.matrix[d]
            yield edge
            yield np.flipud(edge)


def create_tiles(data: str) -> list[Tile]:
    tiles = []
    for tile_str in data.split("\n\n"):
        tile_str = tile_str.splitlines()
        id_str, matrix_str = tile_str[0], tile_str[1:]
        _, idx = id_str.split(" ")
        matrix = np.array([[1 if c == "#" else 0 for c in row] for row in matrix_str])
        tile = Tile(int(idx[:-1]), matrix)
        tiles.append(tile)
    return tiles


def create_grid(tiles: list[Tile]) -> tuple[Grid, int]:
    # collect all possible edges
    edges_to_tiles: defaultdict[EdgeTuple, set[Tile]] = defaultdict(set)
    for tile in tiles:
        for edge in tile.all_symmetry_edges():
            edges_to_tiles[tuple(edge)].add(tile)

    # find edge and corner tiles
    # "..., but the outermost edges won't line up with any other tiles"
    edge_tiles: Counter[Tile] = Counter(tiles.pop() for tiles in edges_to_tiles.values() if len(tiles) == 1)
    corner_tiles: list[Tile] = [tile for tile, count in edge_tiles.items() if count == 4]
    assert len(corner_tiles) == 4, f"Found {len(corner_tiles)} corner tiles, expected 4."
    p1 = prod(tile.idx for tile in corner_tiles)

    # init grid for stitching, y downwards
    dim = int(np.sqrt(len(tiles)))
    assert dim*dim == len(tiles), f"No quadratic shape possible for {len(tiles)} tiles."
    grid: dict[Pos, Tile | None] = {x+y*1j: None for x in range(dim) for y in range(dim)}

    # pick any corner tile as the top left corner
    top_left_corner = corner_tiles[0]
    grid[0] = top_left_corner

    # find correct orientation for the top left corner
    for _ in top_left_corner.transform():
        north_and_west_edges = top_left_corner.get_north_and_west_edges()
        if all(len(edges_to_tiles[tuple(e)]) == 0 for e in north_and_west_edges):  # got popped above
            break
    else:
        raise ValueError("Aligning top left corner failed.")

    # iterate grid
    # y-axis first, then x-axis
    for pos in grid:

        # top left is done
        if pos == 0:
            continue

        # must share edge with north and/or west neighbor
        # those neighbors are already correcly orientated
        shared_edges: list[tuple[Edge, Dir]] = []
        neighbors: set[Tile] = set()
        for d in (DIRS["N"], DIRS["W"]):
            if (neighbor := grid.get(pos+d, None)):
                shared_edge = neighbor.get_edge(-d)  # -d cuz mirrored
                shared_edges.append((shared_edge, d))
                neighbors.add(neighbor)

        candidates: set[Tile] = set()
        for edge, _ in shared_edges:
            candidates.update(edges_to_tiles[tuple(edge)])
        candidates.difference_update(neighbors)

        # only one candidate should be left
        assert len(candidates) == 1, f"No Tile found for position {pos}"
        tile = candidates.pop()

        # find correct transformation
        for _ in tile.transform():
            if all((shared_edge == tile.get_edge(d)).all() for shared_edge, d in shared_edges):
                break
        else:
            raise ValueError(f"Aligning tile {grid[pos]} in position {pos} failed.")

        grid[pos] = tile

    return grid, p1


def create_image(grid: Grid) -> Tile:
    dim_grid = round(np.sqrt(len(grid)))
    dim_tile = grid[0].matrix.shape[0] - 2  # type: ignore
    dim_image = dim_grid * dim_tile
    image = np.zeros((dim_image, dim_image), dtype=int)

    for x, y in product(range(dim_grid), repeat=2):
        pos = x + y*1j
        image[y*dim_tile: (y+1)*dim_tile,
              x*dim_tile: (x+1)*dim_tile] = grid[pos].matrix[1:-1, 1:-1]  # type:ignore

    return Tile(0, image)


def find_sea_monsters(image: Tile) -> int:
    monster = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    ])
    pixel_monster = monster.sum()
    pixel_image = image.matrix.sum()
    for _ in image.transform():
        corr = convolve(image.matrix, monster, mode="constant")
        if (mask_monsters := (corr == pixel_monster)).any():
            break
    else:
        raise ValueError("Could not detect any monster.")

    image.matrix[mask_monsters] = 5
    return pixel_image - mask_monsters.sum() * pixel_monster


def plot_tile(tile: Tile) -> None:
    import matplotlib.pyplot as plt
    plt.imshow(tile.matrix)
    plt.show()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

tiles = create_tiles(data)
grid, p1 = create_grid(tiles)
print("Part 1:", p1)

image = create_image(grid)
p2 = find_sea_monsters(image)
print("Part 2:", p2)


e = timer()
print("time:", e - s)

plot_tile(image)
