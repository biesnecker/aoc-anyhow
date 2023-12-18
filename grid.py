# Assumes that the grid is a hashmap of (x, y) tuples to characters. It calculates the minimum and maximum x and y values, and then iterates over all of the points in the grid. If the point is not in the grid, it yields a space. Otherwise, it yields the character at that point.
def debug_print_grid(
    grid, *, empty=" ", filled=None, padding=0, specialf=None, special=None
):
    (min_x, max_x), (min_y, max_y) = grid_bounds(grid)
    for y in range(min_y - padding, max_y + padding + 1):
        line = []
        for x in range(min_x - padding, max_x + padding + 1):
            if specialf is not None and specialf((x, y)):
                assert special is not None
                line.append(special)
            elif (x, y) not in grid:
                line.append(empty)
            elif filled is not None:
                line.append(filled)
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
