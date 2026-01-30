import os.path
from timeit import default_timer as timer
from collections import deque

type Card = int
type Deck = tuple[int, ...]


def create_decks(data: str) -> tuple[Deck, Deck]:
    p1, p2 = data.split("\n\n")
    deck1 = tuple(int(x) for x in p1.splitlines()[1:])
    deck2 = tuple(int(x) for x in p2.splitlines()[1:])
    return deck1, deck2


def winning_score(deck: deque[int]) -> int:
    return sum(i*card for i, card in enumerate(reversed(deck), 1))


def play_combat(deck1: Deck, deck2: Deck) -> int:
    p1, p2 = deque(deck1), deque(deck2)
    max_rounds = 10**5

    for _ in range(max_rounds):
        card1, card2 = p1.popleft(), p2.popleft()
        if card1 > card2:
            p1.extend((card1, card2))
        else:
            p2.extend((card2, card1))

        if len(p1) == 0 or len(p2) == 0:
            winner = p2 if len(p1) == 0 else p1
            break
    else:
        raise ValueError(f"No Winner after {max_rounds} rounds.")

    return winning_score(winner)


hits = 0
misses = 0
memo: dict[tuple[Deck, Deck], tuple[bool, deque[int]]] = {}


def play_recursive_combat(deck1: Deck, deck2: Deck) -> tuple[bool, deque[int]]:

    # memo check
    global hits, misses, memo
    if (deck1, deck2) in memo:
        hits += 1
        return memo[(deck1, deck2)]
    elif (deck2, deck1) in memo:
        hits += 1
        return memo[(deck2, deck1)]
    else:
        misses += 1

    # init qs and history
    p1, p2 = deque(deck1), deque(deck2)
    history: set[tuple[Deck, Deck]] = set()

    # start playing rounds
    max_rounds = 10**5
    for _ in range(max_rounds):

        # avoid infinite game
        curr_round = (tuple(p1), tuple(p2))
        if curr_round in history:
            memo[(deck1, deck2)] = (True, p1)
            memo[(deck2, deck1)] = (False, p1)
            return True, p1
        history.add(curr_round)

        # draw cards
        card1, card2 = p1.popleft(), p2.popleft()

        # determine round winner
        if len(p1) >= card1 and len(p2) >= card2:
            p1_won, _ = play_recursive_combat(tuple(p1)[:card1], tuple(p2)[:card2])
        else:
            p1_won = True if card1 > card2 else False

        # round winner takes cards
        if p1_won:
            p1.extend((card1, card2))
        else:
            p2.extend((card2, card1))

        # do we have a winner?
        if len(p1) == 0:
            memo[(deck1, deck2)] = (False, p2)
            memo[(deck2, deck1)] = (True, p2)
            return False, p2
        elif len(p2) == 0:
            memo[(deck1, deck2)] = (True, p1)
            memo[(deck2, deck1)] = (False, p1)
            return True, p1
    else:
        raise ValueError(f"No Winner after {max_rounds} rounds.")


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

deck1, deck2 = create_decks(data)
print("Part 1:", play_combat(deck1, deck2))

p1_won, winning_deck = play_recursive_combat(deck1, deck2)
part2 = winning_score(winning_deck)
print("Part 2:", part2)
print("using @cache: CacheInfo(hits=1672, misses=19570, maxsize=None, currsize=19570)")
print(f"using custom cache: hits={hits}, misses={misses}, size={len(memo)}")

e = timer()
print("time:", e - s)
