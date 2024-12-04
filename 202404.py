from collections import deque
from typing import Deque, Dict, Optional, Tuple

from utils import Dir, get_neighbors_all, get_neighbors_diagonal, input_as_strings_iter

letters: Dict[complex, str] = {}
for y, line in enumerate(input_as_strings_iter("202404.txt")):
    for x, char in enumerate(line):
        letters[x + y * 1j] = char

next_char = {"X": "M", "M": "A", "A": "S"}

part_one = 0
# Every X is a potential start point
q: Deque[Tuple[str, complex, Optional[Dir]]] = deque(
    ("X", pos, None) for pos, char in letters.items() if char == "X"
)

while q:
    char, pos, d = q.popleft()
    if char == "S":
        part_one += 1
        continue
    nc = next_char[char]
    if char == "X":
        # For X, next letter can be any direction
        for d, npos in get_neighbors_all(pos):
            if letters.get(npos) == nc:
                q.append((nc, npos, d))
    else:
        assert d is not None
        # next letter must be in the same direction as previous
        npos = pos + d.value
        if letters.get(npos) == nc:
            q.append((nc, npos, d))

print(f"Part one: {part_one}")


part_two = 0
for pos, char in letters.items():
    if char != "A":
        continue
    # Get the corners
    corners = {d: letters.get(npos) for d, npos in get_neighbors_diagonal(pos)}
    if any(not (cv == "M" or cv == "S") for cv in corners.values()):
        # If any of the corners are not M or S, then this is not a valid square
        continue
    if corners[Dir.NORTHEAST] == "M" and corners[Dir.SOUTHWEST] != "S":
        continue
    if corners[Dir.NORTHEAST] == "S" and corners[Dir.SOUTHWEST] != "M":
        continue
    if corners[Dir.NORTHWEST] == "M" and corners[Dir.SOUTHEAST] != "S":
        continue
    if corners[Dir.NORTHWEST] == "S" and corners[Dir.SOUTHEAST] != "M":
        continue
    part_two += 1

print(f"Part two: {part_two}")
