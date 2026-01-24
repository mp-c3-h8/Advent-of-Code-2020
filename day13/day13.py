import os.path
from timeit import default_timer as timer
from math import prod
from z3 import Optimize, Int


def part1(data: list[str]) -> int:
    t = int(data[0])
    res = [((num := int(c))-(t % num), num) for c in data[1].split(",") if c != "x"]
    res.sort()
    return prod(res[0])


def part2(data: list[str]) -> int:
    # "simple" Integer Linear Programming
    # scipy optimize would also do, but z3 doesnt need matrices..
    solver = Optimize()
    t = Int("t")
    solver.add(t > 0)
    for i, bus_id in enumerate(data[1].split(",")):
        if bus_id == "x":
            continue
        x = Int(f"x{i}")
        solver.add(x > 0)
        solver.add(t == int(bus_id)*x - i)
    solver.minimize(t)
    assert (repr(solver.check()) == "sat"), "No optimal solution found"
    res = solver.model()[t].as_long()  # type: ignore
    return int(res)


# CRT: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
# https://www.geeksforgeeks.org/dsa/chinese-remainder-theorem-in-python/
def part2_crt(data: list[str]) -> int:

    def gcd_extended(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def find_min_x(num: list[int], rem: list[int]) -> int:
        N = prod(num)
        result = 0
        for i in range(len(num)):
            prod_i = N // num[i]
            _, inv_i, _ = gcd_extended(prod_i, num[i])
            result += rem[i] * prod_i * inv_i

        return result % N

    num, rem = [], []
    for i, bus_id in enumerate(data[1].split(",")):
        if bus_id == "x":
            continue
        num.append(int(bus_id))
        rem.append(-i)

    return find_min_x(num, rem)


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

print("Part 1:", part1(data))
print("Part 2:", part2(data))
print("Part 2 (CRT):", part2_crt(data))


e = timer()
print("time:", e - s)
