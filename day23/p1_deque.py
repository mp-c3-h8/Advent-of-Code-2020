import os.path
from timeit import default_timer as timer
from collections import deque
from itertools import combinations, permutations
from math import prod

type Cup = int
type Cups = list[int]
type Circle = deque[int]
type DestinationLookup = dict[tuple[Cup, tuple[Cup, ...]], Cup]


def precalc_destination(cups: Cups) -> DestinationLookup:
    cups = sorted(cups)
    low = cups[0]
    high = cups[-1]
    destinations = {}

    cups_set = set(cups)
    for curr in cups:
        rest = cups_set.difference({curr})
        for three_cups in combinations(rest, 3):
            pool = rest.difference(three_cups)
            dest = curr
            while dest not in pool:
                dest = high if dest == low else dest-1
            for perm in permutations(three_cups, 3):
                destinations[(curr, perm)] = dest

    # sanity check
    n = len(cups)
    expected = prod(n-k for k in range(4))
    assert len(destinations) == expected, "Misscalculated destinations"

    return destinations


def rotate_to(circle: Circle, target: Cup) -> None:
    idx = circle.index(target)
    circle.rotate(-(idx+1))


def play_cup_game(cups: Cups, moves: int) -> str:
    destinations = precalc_destination(cups)
    circle: Circle = deque(cups)
    curr: Cup = cups[0]

    for i in range(moves):
        rotate_to(circle, curr)
        pick_up = tuple(circle.popleft() for _ in range(3))
        dest = destinations[(curr, pick_up)]
        curr = circle[0]
        rotate_to(circle, dest)
        circle.extend(pick_up)
        # print(f"move {i+1} -> curr: {curr}, pick up: {pick_up}, dest: {dest}, circle: {list(circle)}, ")

    # calc answer
    rotate_to(circle, 1)
    res = "".join(str(n) for n in circle)
    return res[:-1]


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

cups = list(map(int, data))
assert (len(cups)) >= 5, "Need at least five cups to play the game"
p1 = play_cup_game(cups, 100)
print("Part 1:", p1)

e = timer()
print("time:", e - s)
