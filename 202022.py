from functools import cache

with open("202022.txt", "r") as f:
    lines = f.read().strip().split("\n\n")
    player1 = tuple(map(int, lines[0].splitlines()[1:]))
    player2 = tuple(map(int, lines[1].splitlines()[1:]))


@cache
def play_game(player1, player2):
    while player1 and player2:
        p1 = player1[0]
        p2 = player2[0]
        if p1 > p2:
            player1 = player1[1:] + (p1, p2)
            player2 = player2[1:]
        else:
            player1 = player1[1:]
            player2 = player2[1:] + (p2, p1)
    return player1 or player2


def score(deck):
    return sum((i + 1) * card for i, card in enumerate(reversed(deck)))


print(f"Part one: {score(play_game(player1, player2))}")


@cache
def play_game_recursive(player1, player2):
    seen = set()
    while player1 and player2:
        if (player1, player2) in seen:
            return True, player1
        seen.add((player1, player2))
        p1 = player1[0]
        p2 = player2[0]
        if len(player1) > p1 and len(player2) > p2:
            player_one_wins, _ = play_game_recursive(
                player1[1 : p1 + 1], player2[1 : p2 + 1]
            )
        else:
            player_one_wins = p1 > p2
        if player_one_wins:
            player1 = player1[1:] + (p1, p2)
            player2 = player2[1:]
        else:
            player1 = player1[1:]
            player2 = player2[1:] + (p2, p1)
    player_one_wins = len(player1) > 0
    return player_one_wins, player1 if player_one_wins else player2


print(f"Part two: {score(play_game_recursive(player1, player2)[1])}")
