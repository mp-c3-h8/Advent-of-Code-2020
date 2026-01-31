import os.path
from timeit import default_timer as timer

type Circle = list[Cup]


class Cup:
    __slots__ = ('val', 'nxt')

    def __init__(self, val: int, nxt: Cup) -> None:
        self.val: int = val
        self.nxt: Cup = nxt


class DummyCup(Cup):
    __slots__ = ('val', 'nxt')

    def __init__(self) -> None:
        self.val = 0
        self.nxt = self


def create_circle(initial: list[int], total: int | None = None) -> Circle:
    total = len(initial) if not total else total
    assert total >= len(initial), f"Cant fill up to {total} cups with {len(initial)} initially given"
    dummy = DummyCup()
    circle: Circle = [dummy]*(len(initial)+1)

    last = 0
    for num in initial:
        cup = Cup(num, dummy)
        circle[num] = cup  # important: cup id in circle == cup val
        circle[last].nxt = cup
        last = num

    for num in range(len(initial)+1, total+1):
        cup = Cup(num, dummy)
        circle.append(cup)
        circle[last].nxt = cup
        last = num

    circle[last].nxt = circle[initial[0]]
    return circle


def part1(circle: Circle) -> str:
    curr = circle[1].nxt
    res = ""
    for _ in range(len(circle)-2):
        res += str(curr.val)
        curr = curr.nxt
    return res


def part2(circle: Circle) -> int:
    return circle[1].nxt.val * circle[1].nxt.nxt.val


def play_cup_game(circle: Circle, curr: Cup, moves: int):
    max_value = len(circle)-1

    for _ in range(moves):
        pick_up_begin: Cup = curr.nxt
        pick_up_end: Cup = curr.nxt.nxt.nxt

        dest_val = curr.val
        while True:
            dest_val = max_value if dest_val == 1 else dest_val-1
            if (
                dest_val != pick_up_begin.val and
                dest_val != pick_up_begin.nxt.val and
                dest_val != pick_up_end.val
            ):
                break

        # cup id in circle == cup val
        dest: Cup = circle[dest_val]

        curr.nxt = pick_up_end.nxt
        pick_up_end.nxt = dest.nxt
        dest.nxt = pick_up_begin
        curr = curr.nxt


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

initial = list(map(int, data))
start = initial[0]

circle = create_circle(initial)
play_cup_game(circle, circle[start], 100)
print("Part 1:", part1(circle))

circle = create_circle(initial, 1_000_000)
play_cup_game(circle, circle[start], 10_000_000)
print("Part 2:", part2(circle))


e = timer()
print("time:", e - s)
