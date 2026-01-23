import os.path
from timeit import default_timer as timer

type Pos = complex  # y upwards
type Dir = complex  # |d| = 1

DIRS: dict[str, Dir] = {
    "N": 1j,
    "S": -1j,
    "E": 1,
    "W": -1
}

ROTATIONS: dict[int, Dir] = {
    90: 1j,
    180: -1,
    270: -1j
}


def part1(instr: list[str]) -> int:
    global DIRS, ROTATIONS
    pos = 0
    d = 1  # facing east
    for inst in instr:
        action, value = inst[0], int(inst[1:])
        match action:
            case "L":
                d *= ROTATIONS[value]
            case "R":
                d *= ROTATIONS[value].conjugate()
            case "F":
                pos += value*d
            case _:  # N,S,E,W
                pos += value*DIRS[action]
    return int(abs(pos.real) + abs(pos.imag))


def part2(instr: list[str]) -> int:
    global DIRS, ROTATIONS
    ship_pos = 0
    wp_pos = 10 + 1j  # 10 units east and 1 unit north
    for inst in instr:
        action, value = inst[0], int(inst[1:])
        match action:
            case "L":
                wp_pos *= ROTATIONS[value]
            case "R":
                wp_pos *= ROTATIONS[value].conjugate()
            case "F":
                ship_pos += value*wp_pos
            case _:  # N,S,E,W
                wp_pos += value*DIRS[action]
    return int(abs(ship_pos.real) + abs(ship_pos.imag))


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

print("Part 1:", part1(data))
print("Part 2:", part2(data))

e = timer()
print("time:", e - s)
