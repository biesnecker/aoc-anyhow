from functools import cache

cards = {}

with open("202304.txt", "r") as f:
    for line in f:
        [card_id, card] = line.strip().split(": ")
        card_id = int(card_id.split()[1])
        [winning, nums] = card.split(" | ")
        winning = set(map(int, winning.split()))
        nums = set(map(int, nums.split()))
        cards[card_id] = (winning, nums)

scores = {card_id: len(winning & nums) for card_id, (winning, nums) in cards.items()}

part_one = 0
for score in scores.values():
    if score > 0:
        part_one += 2 ** (score - 1)
print(f"Part one: {part_one}")


@cache
def n_cards_for_cards(card_id):
    score = scores[card_id]
    if score == 0:
        return 1
    else:
        return 1 + sum(
            n_cards_for_cards(i) for i in range(card_id + 1, card_id + 1 + score)
        )


part_two = sum(n_cards_for_cards(card_id) for card_id in cards.keys())
print(f"Part two: {part_two}")
