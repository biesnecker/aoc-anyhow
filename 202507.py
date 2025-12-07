from functools import cache

from utils import coord_to_xy, move_east, move_south, move_west, xy_to_coord

lines = open("202507.txt").read().splitlines()
splitters = {
    xy_to_coord(x, y)
    for y, line in enumerate(lines)
    for x, c in enumerate(line)
    if c == "^"
}
start = next(xy_to_coord(x, 0) for x, c in enumerate(lines[0]) if c == "S")
max_y = max(coord_to_xy(s)[1] for s in splitters)

visited = set()


@cache
def solve(pos):
    if coord_to_xy(pos)[1] > max_y:
        return 1

    nxt = move_south(pos)
    if nxt in splitters:
        visited.add(nxt)
        return solve(move_west(nxt)) + solve(move_east(nxt))
    else:
        return solve(nxt)


part2 = solve(start)
part1 = len(visited)
print(part1)
print(part2)
