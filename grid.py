# Assumes that the grid is a hashmap of (x, y) tuples to characters. It calculates the minimum and maximum x and y values, and then iterates over all of the points in the grid. If the point is not in the grid, it yields a space. Otherwise, it yields the character at that point.
def debug_print_grid(grid, *, empty=" "):
    (min_x, max_x), (min_y, max_y) = grid_bounds(grid)
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if (x, y) not in grid:
                line.append(empty)
            else:
                line.append(grid[(x, y)])
        print("".join(line))
    print("", flush=True)


def grid_bounds(grid):
    min_x = min(x for (x, _) in grid.keys())
    max_x = max(x for (x, _) in grid.keys())
    min_y = min(y for (_, y) in grid.keys())
    max_y = max(y for (_, y) in grid.keys())
    return ((min_x, max_x), (min_y, max_y))
