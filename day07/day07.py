import os.path
from functools import cache

type Color = str
type Rules = dict[str, list[tuple[int, str]]]


def create_rules(data: str) -> Rules:
    rules: dict[Color, list[tuple[int, str]]] = {}
    for line in data.splitlines():
        key_str, values_str = line.split(" contain ")
        key = key_str[:-5]
        values = []
        if values_str[:2] != "no":
            for value_str in values_str.split(", "):
                num_str, *color, _ = value_str.split(" ")
                values.append((int(num_str), " ".join(color)))
        rules[key] = values
    return rules


@cache
def valid(goal: Color, color: Color) -> bool:
    global rules
    if color == goal:
        return True
    return any(valid(goal, c) for num, c in rules[color])


@cache
def required_bags(color: Color) -> int:
    global rules
    return sum(num + num*required_bags(c) for num, c in rules[color])


def part1(rules: Rules, goal: Color) -> int:
    return sum(valid(goal, color) for color in rules if color != goal)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

rules: Rules = create_rules(data)
print("Part 1:", part1(rules, "shiny gold"))
print("Part 2:", required_bags("shiny gold"))
