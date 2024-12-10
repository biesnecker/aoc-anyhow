from utils import get_neighbors_cardinal, input_as_strings_iter, xy_to_coord

grid = {}
for y, row in enumerate(input_as_strings_iter("202410.txt")):
    for x, c in enumerate(row):
        grid[xy_to_coord(x, y)] = int(c)


def solve(unique: bool = False) -> int:
    starts = [c for c, v in grid.items() if v == 0]

    def bfs(start: complex) -> int:
        visited = set()
        q = [start]
        visited.add(start)
        res = 0
        while q:
            pos = q.pop(0)
            v = grid[pos]
            if v == 9:
                res += 1
            ns = v + 1
            for _, npos in get_neighbors_cardinal(pos):
                if (unique or npos not in visited) and grid.get(npos, -1) == ns:
                    if not unique:
                        visited.add(npos)
                    q.append(npos)
        return res

    return sum(bfs(s) for s in starts)


print(f"Part one: {solve()}")
print(f"Part two: {solve(unique=True)}")
