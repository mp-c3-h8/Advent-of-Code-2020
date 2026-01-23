import os.path
from timeit import default_timer as timer

type Pos = tuple[int, int]  # (y,x)
type Grid = dict[Pos, bool]  # { (y,x): occupied? }
type Neighborhood = dict[Pos, list[Pos]]

DIRS8 = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]



s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()


empty: Grid = {(y, x): False for y, row in enumerate(data) for x, c in enumerate(row) if c == "L"}
dimy, dimx = len(data), len(data[0])



e = timer()
print("time:", e - s)
