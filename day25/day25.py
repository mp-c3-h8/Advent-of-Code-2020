import os.path
from timeit import default_timer as timer


def decode(subject: int, public_key: int) -> int:
    val: int = 1
    for n in range(10**8):
        val *= subject
        val %= 20201227
        if val == public_key:
            return n+1
    else:
        raise ValueError("Max iterations reached")


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

door_public = int(data[0])
card_public = int(data[1])

door_loop = decode(7, door_public)
# card_loop = decode(7, card_public)

encryption_key = pow(card_public, door_loop, 20201227)
print("Part 1:", encryption_key)


e = timer()
print(f"time: {e-s}")
