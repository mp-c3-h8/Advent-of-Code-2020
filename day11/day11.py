import os.path
from timeit import default_timer as timer

type Pos = tuple[int, int]  # (y,x)
type Grid = dict[Pos, bool]  # { (y,x): occupied? }
type Neighborhood = dict[Pos, list[Pos]]

DIRS8 = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]


def add(x: Pos, y: Pos) -> Pos:
    return (x[0]+y[0], x[1]+y[1])


def precompute_neighborhood(grid: Grid, dimy: int, dimx: int, part2: bool = False) -> Neighborhood:
    if not part2:
        return {pos: [n for d in DIRS8 if (n := add(pos, d)) in grid] for pos in grid}

    # part 2
    res = {}
    for pos in grid:
        neighbors = []
        for d in DIRS8:
            n = add(pos, d)
            while (0 <= n[1] < dimx and 0 <= n[0] < dimy):
                if n in grid:
                    neighbors.append(n)
                    break
                n = add(n, d)
        res[pos] = neighbors
    return res


def sim(grid: Grid, neighborhood: Neighborhood, tolarance: int) -> Grid:
    new_grid: Grid = {}
    for pos, state in grid.items():
        num_neighbors = sum([grid[n] for n in neighborhood[pos]])
        if state:  # occupied
            new_grid[pos] = num_neighbors < tolarance
        else:  # empty
            new_grid[pos] = num_neighbors == 0

    return new_grid


def equilibrium(grid: Grid, neighborhood: Neighborhood, tolarance: int) -> int:
    while grid != (grid := sim(grid, neighborhood, tolarance)):
        pass
    return sum(grid.values())


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()


empty: Grid = {(y, x): False for y, row in enumerate(data) for x, c in enumerate(row) if c == "L"}
dimy, dimx = len(data), len(data[0])

neighborhood_p1 = precompute_neighborhood(empty, dimy, dimx)
p1 = equilibrium(empty, neighborhood_p1, 4)
print("Part 1:", p1)

neighborhood_p2 = precompute_neighborhood(empty, dimy, dimx, part2=True)
p2 = equilibrium(empty, neighborhood_p2, 5)
print("Part 2:", p2)

e = timer()
print("time:", e - s)
