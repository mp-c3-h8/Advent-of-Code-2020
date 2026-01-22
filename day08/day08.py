import os.path

type Instruction = tuple[str, int]
type Program = list[Instruction]


def operate(instr: Instruction, acc: int, idx: int) -> tuple[int, int]:
    op, arg = instr
    match op:
        case "acc":
            acc += arg
            idx += 1
        case "jmp":
            idx += arg
        case "nop":
            idx += 1
    return acc, idx


def part1(program: Program, acc: int = 0, idx: int = 0) -> tuple[bool, int]:
    seen = set()
    while True:
        if idx in seen or idx > len(program):
            return False, acc
        if idx == len(program):
            return True, acc
        seen.add(idx)
        acc, idx = operate(program[idx], acc, idx)


def part2(program: Program) -> int:
    acc = idx = 0
    seen = set()
    while True:
        if idx in seen or idx > len(program):
            raise ValueError("Cant fix program.")

        # fork on jmp or nop operations
        op, arg = program[idx]
        if op != "acc":
            new_op = "jmp" if op == "nop" else "nop"
            new_acc, new_idx = operate((new_op, arg), acc, idx)
            success, new_acc = part1(program, new_acc, new_idx)
            if success:
                return new_acc

        # continue execution
        seen.add(idx)
        acc, idx = operate(program[idx], acc, idx)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

program: Program = [(line[:3], int(line[4:])) for line in data]

_, p1 = part1(program)
print("Part 1:", p1)

print("Part 2:", part2(program))
