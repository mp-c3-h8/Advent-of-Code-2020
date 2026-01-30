import os.path
from timeit import default_timer as timer
from collections import Counter

type Ingredient = str  # i.e. mxmxvkd
type Allergen = str  # i.e. dairy


# could be done with https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm
# Bipartite Matching
def solve(data: str) -> tuple[int, str]:

    # possibilities for every allergen
    possibilities: dict[Allergen, set[Ingredient]] = {}
    ingredient_count: Counter[Ingredient] = Counter()

    for line in data.splitlines():
        lhs, rhs = line.split(" (contains ")
        ingre: list[Ingredient] = lhs.split(" ")
        aller: list[Allergen] = rhs[:-1].split(", ")
        ingredient_count.update(ingre)
        for a in aller:
            if a in possibilities:
                possibilities[a].intersection_update(ingre)
            else:
                possibilities[a] = set(ingre)

    for ingredients in possibilities.values():
        for i in ingredients:
            if i in ingredient_count:
                del ingredient_count[i]

    p1 = ingredient_count.total()
    done: list[tuple[Allergen, Ingredient]] = []

    # consecutively reduce every set to size 1
    while len(possibilities) > 0:
        # do we have a single element set?
        for a, ingredients in possibilities.items():
            if len(ingredients) == 1:
                found = ingredients.pop()
                done.append((a, found))
                del possibilities[a]
                break
        # no further progress possible
        else:
            raise ValueError("Cant find all Allergens")

        # remove newly found entry from other sets
        for ingredients in possibilities.values():
            ingredients.difference_update({found})

    done = sorted(done)
    p2 = ",".join(d[1] for d in done)

    return p1, p2


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

p1, p2 = solve(data)
print("Part 1:", p1)
print("Part 2:", p2)


e = timer()
print("time:", e - s)
