import os.path
from timeit import default_timer as timer
from operator import add, mul

OP = {"+": add, "*": mul}


def homework(data: list[str]) -> int:
    stack = []

    def evaluate(expr: str) -> int:
        nonlocal stack
        if expr.isdigit():
            return int(expr)
        elif expr[0] in "+*":
            return OP[expr[0]](stack.pop(), evaluate(expr[1:]))
        elif expr[0].isdigit():
            idx = 0
            while expr[idx].isdigit():
                idx += 1
            stack.append(int(expr[:idx]))
            return evaluate(expr[idx:])
        else:  # brackets
            bracket = expr[0]
            opposite = ")" if bracket == "(" else "("
            idx = 1
            count = 1
            while count != 0:
                if expr[idx] == opposite:
                    count -= 1
                elif expr[idx] == bracket:
                    count += 1
                idx += 1
            return evaluate(str(evaluate(expr[1:idx-1])) + expr[idx:])

    res = 0
    for line in data:
        line = line.replace(" ", "")
        ee = evaluate(line[::-1])
        res += ee
    return res



s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

print("Part 1:", homework(data))


e = timer()
print("time:", e - s)
