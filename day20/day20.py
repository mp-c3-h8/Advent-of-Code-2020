import os.path
from timeit import default_timer as timer
import numpy as np
from typing import Iterator
from collections import defaultdict, Counter
from math import prod

type Orientation = tuple[int, int]  # (a,b), a: number of rot90 in {0,1,2,3}, b: fliplr yes/no in {0,1}
type Pos = complex  # y = i downwards
type Dir = complex
type Grid = dict[Pos, Tile | None]

DIRS: dict[str, Dir] = {"N": -1j, "E": 1, "S": 1j, "W": -1}


class Image:
    def __init__(self, tiles: list[Tile]) -> None:
        self.tiles = tiles
        self.dim = int(np.sqrt(len(tiles)))
        assert self.dim*self.dim == len(tiles), f"No quadratic shape possible for {len(tiles)} tiles."

    def __repr__(self) -> str:
        return str(self.tiles)


class Tile:
    def __init__(self, idx: int, matrix: np.ndarray) -> None:
        self.idx = idx
        self.matrix = matrix
        self.orientation: Orientation = (-1, -1)

    # https://en.wikipedia.org/wiki/Dihedral_group_of_order_8
    def symmetries(self) -> Iterator[tuple[np.ndarray, Orientation]]:
        a = self.matrix
        for k in range(4):
            yield a, (k, 0)
            yield np.fliplr(a), (k, 1)
            a = np.rot90(a)

    def north_and_west_edges(self) -> Iterator[tuple[list[np.ndarray], Orientation]]:
        for a, o in self.symmetries():
            yield [a[0, :], a[:, 0]], o

    # get oriented matrix
    def oriented(self) -> np.ndarray:
        assert (self.orientation is not None)
        rot, flip = self.orientation
        a = np.rot90(self.matrix, rot)
        return a if flip == 0 else np.fliplr(a)

    # 8 different edges for all symmetries
    def symmetry_edges(self) -> Iterator[np.ndarray]:
        a = self.matrix
        yield (N := a[0, :])  # N
        yield np.flipud(N)
        yield (W := a[:, 0])  # W
        yield np.flipud(W)
        yield (S := a[-1, :])  # S
        yield np.flipud(S)
        yield (E := a[:, -1])  # E
        yield np.flipud(E)

    def __repr__(self) -> str:
        return str(self.idx)


def init_image(data: str) -> Image:
    tiles = []
    for tile_str in data.split("\n\n"):
        tile_str = tile_str.splitlines()
        id_str, matrix_str = tile_str[0], tile_str[1:]
        _, idx = id_str.split(" ")
        matrix = np.array([[1 if c == "#" else 0 for c in row] for row in matrix_str])
        tile = Tile(int(idx[:-1]), matrix)
        tiles.append(tile)
    return Image(tiles)


def get_edge(matrix: np.ndarray, d: Dir) -> np.ndarray:
    match d:
        case -1j: return matrix[0, :]   # N
        case   1: return matrix[:, -1]  # E
        case  1j: return matrix[-1, :]  # S
        case -1: return matrix[:, 0]    # W
    raise ValueError(f"Direction {d} not defined")


def get_wanted_edges(grid: Grid, pos: Pos) -> list[np.ndarray | None]:
    res = []
    for d in (DIRS["N"], DIRS["W"]):
        n = pos+d
        if n in grid and grid[n] is not None:
            res.append(get_edge(grid[n].oriented(), -d))
        else:
            res.append(None)
    return res


def solve(image: Image) -> None:
    # collect all possible edges
    edges: defaultdict[tuple[int], list[Tile]] = defaultdict(list)
    for tile in image.tiles:
        for edge in tile.symmetry_edges():
            edges[tuple(edge)].append(tile)

    # find edge and corner tiles
    # "..., but the outermost edges won't line up with any other tiles"
    edge_tiles: Counter[Tile] = Counter(tiles[0] for edge, tiles in edges.items() if len(tiles) == 1)
    corner_tiles: list[Tile] = [tile for tile, count in edge_tiles.items() if count == 4]
    assert len(corner_tiles) == 4, f"Found {len(corner_tiles)} corner tiles, expected 4."
    print("Part 1:", prod(tile.idx for tile in corner_tiles))

    # init grid for stitching, y downwards
    dim = image.dim
    grid: dict[Pos, Tile | None] = {x+y*1j: None for x in range(dim) for y in range(dim)}

    # pick any corner tile as the top left corner
    grid[0] = corner_tiles[0]

    # find correct orientation for the top left corner
    for symmetry, orientation in grid[0].symmetries():
        north_edge = get_edge(symmetry, DIRS["N"])
        west_edge = get_edge(symmetry, DIRS["W"])
        if len(edges[tuple(north_edge)]) == 1 == len(edges[tuple(west_edge)]):
            break
    else:
        raise ValueError("Aligning top left corner failed.")
    grid[0].orientation = orientation

    # iterate grid
    for pos in grid:

        # top left is done
        if pos == 0:
            continue

        # must share edge with north/west neighbor
        # those neighbors are already correcly orientated
        shared_edges = []
        neighbors = set()
        for d in (DIRS["N"], DIRS["W"]):
            if (neighbor := grid.get(pos+d, None)):
                shared_edge = get_edge(neighbor.oriented(), -d)
                shared_edges.append(tuple(shared_edge))
                neighbors.add(neighbor)

        candidates = set()
        for edge in shared_edges:
            candidates.update(edges[edge])
        candidates.difference_update(neighbors)

        # only one candidate should be left
        assert len(candidates) == 1, f"No Tile found for position {pos}"
        tile: Tile = list(candidates)[0]

        # find correct orientation
        wanted_edges = get_wanted_edges(grid, pos)
        # print(wanted_edges)

        for transformed_edges, orientation in tile.north_and_west_edges():
            if all((a is None) or (b is None) or (a == b).all() for a, b in zip(wanted_edges, transformed_edges)):
                break
        else:
            raise ValueError(f"Aligning tile {grid[pos]} in position {pos} failed.")

        tile.orientation = orientation
        grid[pos] = tile

    print(grid)


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

image = init_image(data)
solve(image)

e = timer()
print("time:", e - s)
