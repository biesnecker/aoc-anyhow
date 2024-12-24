import math
from collections import defaultdict

games = {}
with open("202302.txt", "r") as f:
    for line in f:
        [game_id, matchesRaw] = line.strip().split(": ")
        game_id = int(game_id.split(" ")[1])
        matches = []
        for match in matchesRaw.split("; "):
            this_match = {}
            for move in match.split(", "):
                [count, color] = move.split(" ")
                this_match[color] = int(count)
            matches.append(this_match)
        games[game_id] = matches

print(games[1])

maxRed = 12
maxGreen = 13
maxBlue = 14

part_one = 0
for id, matches in games.items():
    for match in matches:
        if (
            match.get("red", 0) > maxRed
            or match.get("green", 0) > maxGreen
            or match.get("blue", 0) > maxBlue
        ):
            break
    else:
        part_one += id
print(f"Part one: {part_one}")

part_two = 0
for matches in games.values():
    needed = defaultdict(int)
    for match in matches:
        for color, count in match.items():
            if count > needed[color]:
                needed[color] = count
    part_two += math.prod(needed.values())
print(f"Part two: {part_two}")
