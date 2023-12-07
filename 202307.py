from collections import Counter
from enum import IntEnum

cards = []

with open("202307.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        cards.append((parts[0], int(parts[1])))


class Hand(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def card_value(card, jokers=False):
    if card.isdigit():
        return int(card)
    elif card == "T":
        return 10
    elif card == "J":
        return 1 if jokers else 11
    elif card == "Q":
        return 12
    elif card == "K":
        return 13
    elif card == "A":
        return 14
    else:
        raise ValueError(f"Invalid card: {card}")


def to_sort_key(cards, jokers=False):
    cc = Counter(cards)
    n_jokers = 0
    if jokers:
        n_jokers = cc["J"]
        del cc["J"]
    match list(sorted(cc.values(), reverse=True)):
        case [5]:
            res = Hand.FIVE_OF_A_KIND
        case [4, *_]:
            res = Hand.FOUR_OF_A_KIND
        case [3, 2]:
            res = Hand.FULL_HOUSE
        case [3, *_]:
            res = Hand.THREE_OF_A_KIND
        case [2, 2, *_]:
            res = Hand.TWO_PAIR
        case [2, *_]:
            res = Hand.ONE_PAIR
        case _:
            res = Hand.HIGH_CARD
    if jokers:
        if n_jokers == 5:
            res = Hand.FIVE_OF_A_KIND
        else:
            while n_jokers > 0:
                match res:
                    case Hand.FIVE_OF_A_KIND:
                        raise ValueError("Too many jokers")
                    case Hand.FOUR_OF_A_KIND:
                        res = Hand.FIVE_OF_A_KIND
                    case Hand.FULL_HOUSE:
                        raise ValueError("Too many jokers")
                    case Hand.THREE_OF_A_KIND:
                        res = Hand.FOUR_OF_A_KIND
                    case Hand.TWO_PAIR:
                        res = Hand.FULL_HOUSE
                    case Hand.ONE_PAIR:
                        res = Hand.THREE_OF_A_KIND
                    case Hand.HIGH_CARD:
                        res = Hand.ONE_PAIR
                n_jokers -= 1
    [a, b, c, d, e] = [card_value(x, jokers) for x in cards]
    return (res, a, b, c, d, e)


part_one = 0
for (_, bid), pos in zip(
    sorted(cards, key=lambda x: to_sort_key(x[0])), range(1, len(cards) + 1)
):
    part_one += bid * pos
print(f"Part one: {part_one}")

part_two = 0
for (_, bid), pos in zip(
    sorted(cards, key=lambda x: to_sort_key(x[0], True)), range(1, len(cards) + 1)
):
    part_two += bid * pos
print(f"Part two: {part_two}")
