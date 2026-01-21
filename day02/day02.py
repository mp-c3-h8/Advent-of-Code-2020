import os.path
import re


def solve(data: list[str]) -> tuple[int, int]:
    p1 = p2 = 0
    regex = re.compile(r"\d+")
    for line in data:
        policy, pwd = line.split(": ")
        letter = policy[-1]
        l_min, l_max = map(int, regex.findall(policy))
        if l_min <= pwd.count(letter) <= l_max:
            p1 += 1
        if (pwd[l_min-1] == letter) ^ (pwd[l_max-1] == letter):  # XOR
            p2 += 1
    return p1, p2


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

p1, p2 = solve(data)
print("Part 1:", p1)
print("Part 2:", p2)
