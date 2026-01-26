import os.path
from timeit import default_timer as timer


def memory_game(numbers: list[int], num_turns: int) -> int:

    assert (num_turns > 0), "Number of turns must be positive"
    if num_turns <= len(numbers):
        return numbers[num_turns-1]

    memory: dict[int, int] = {n: i for i, n in enumerate(numbers, 1)}
    last_spoken = numbers[-1]
    for turn in range(len(numbers), num_turns):

        # what to say?
        spoken = turn - memory.get(last_spoken, turn)

        # update memory
        memory[last_spoken] = turn

        last_spoken = spoken

    return last_spoken


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

numbers = [int(c) for c in data.split(",")]
print("Part 1:", memory_game(numbers, 2020))
print("Part 2:", memory_game(numbers, 30_000_000))

e = timer()
print("time:", e - s)
