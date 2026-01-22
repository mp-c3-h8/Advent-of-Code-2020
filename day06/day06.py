import os.path
from collections import Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


groups = data.split("\n\n")
p1 = sum(len(set(group.replace("\n", ""))) for group in groups)
print("Part 1:", p1)

p2 = sum(sum(count == len(group.splitlines())
         for count in Counter(group.replace("\n", "")).values()) for group in groups)
print("Part 2:", p2)
