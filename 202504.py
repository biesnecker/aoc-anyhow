from collections import deque

from utils import get_neighbors_all, xy_to_coord

with open("202504.txt", "r") as f:
    rolls = {
        xy_to_coord(x, y)
        for y, line in enumerate(f)
        for x, c in enumerate(line.strip())
        if c == "@"
    }

neighbors = {c: sum(n in rolls for _, n in get_neighbors_all(c)) for c in rolls}
seen = {c for c in rolls if neighbors[c] < 4}
print(len(seen))

q, part2 = deque(seen), 0
while q:
    part2 += 1
    for _, n in get_neighbors_all(q.popleft()):
        if n in neighbors:
            neighbors[n] -= 1
            if neighbors[n] < 4 and n not in seen:
                seen.add(n)
                q.append(n)
print(part2)
