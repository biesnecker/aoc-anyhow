import itertools

grid = {}
with open("202311.txt", "r") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            if char == "#":
                grid[(x, y)] = char


def find_distances(grid, expansion_factor):
    min_x = min(x for (x, _) in grid.keys())
    max_x = max(x for (x, _) in grid.keys())
    min_y = min(y for (_, y) in grid.keys())
    max_y = max(y for (_, y) in grid.keys())

    empty_cols = set()
    for x in range(min_x, max_x + 1):
        if all((x, y) not in grid for y in range(min_y, max_y + 1)):
            empty_cols.add(x)
    empty_rows = set()
    for y in range(min_y, max_y + 1):
        if all((x, y) not in grid for x in range(min_x, max_x + 1)):
            empty_rows.add(y)

    total = 0
    for (ix, iy), (jx, jy) in itertools.combinations(grid.keys(), 2):
        [min_x, max_x] = sorted([ix, jx])
        [min_y, max_y] = sorted([iy, jy])
        total += (max_x - min_x) + sum(
            expansion_factor - 1 for x in range(min_x, max_x + 1) if x in empty_cols
        )
        total += (max_y - min_y) + sum(
            expansion_factor - 1 for y in range(min_y, max_y + 1) if y in empty_rows
        )
    return total


print(f"Part one: {find_distances(grid, 2)}")
print(f"Part two: {find_distances(grid, 1000000)}")
