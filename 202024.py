from enum import IntEnum


class Direction(IntEnum):
    E = 0
    SE = 1
    SW = 2
    W = 3
    NW = 4
    NE = 5


def parse_directions(line):
    d = []
    prev = None
    for i, c in enumerate(line):
        match (prev, c):
            case (None, "n"):
                prev = "n"
            case (None, "s"):
                prev = "s"
            case (None, "e"):
                d.append(Direction.E)
            case (None, "w"):
                d.append(Direction.W)
            case ("n", "e"):
                d.append(Direction.NE)
                prev = None
            case ("n", "w"):
                d.append(Direction.NW)
                prev = None
            case ("s", "e"):
                d.append(Direction.SE)
                prev = None
            case ("s", "w"):
                d.append(Direction.SW)
                prev = None
            case _:
                raise ValueError(f"Invalid direction: {(prev, c)}")
    assert prev is None
    return d


def move_direction(c, direction):
    match (direction, c):
        case (Direction.E, (q, r, s)):
            return (q + 1, r, s - 1)
        case (Direction.SE, (q, r, s)):
            return (q, r + 1, s - 1)
        case (Direction.SW, (q, r, s)):
            return (q - 1, r + 1, s)
        case (Direction.W, (q, r, s)):
            return (q - 1, r, s + 1)
        case (Direction.NW, (q, r, s)):
            return (q, r - 1, s + 1)
        case (Direction.NE, (q, r, s)):
            return (q + 1, r - 1, s)
        case _:
            raise ValueError(f"Invalid direction: {direction}")


with open("202024.txt", "r") as f:
    moves = [parse_directions(line.strip()) for line in f]

grid = set()
for move in moves:
    c = (0, 0, 0)
    for direction in move:
        c = move_direction(c, direction)
    if c not in grid:
        grid.add(c)
    else:
        grid.remove(c)
print(f"Part one: {len(grid)}")


def adjacent(c):
    q, r, s = c
    yield (q + 1, r - 1, s)
    yield (q - 1, r + 1, s)
    yield (q + 1, r, s - 1)
    yield (q - 1, r, s + 1)
    yield (q, r + 1, s - 1)
    yield (q, r - 1, s + 1)


# At this point grid contains all the coordinates of black tiles. We need to
# consider all the of black tiles, and also all of the white tiles adjacent to
# black tiles. We can do this with some set operations.
for _ in range(100):
    new_grid = set()
    for c in grid:
        # Any black tile with zero or more than 2 black tiles immediately
        # adjacent to it is flipped to white.
        if sum(adj in grid for adj in adjacent(c)) in (1, 2):
            new_grid.add(c)
        # Any white tile with exactly 2 black tiles immediately adjacent to it
        # is flipped to black.
        for adj in adjacent(c):
            if adj not in grid and sum(adj2 in grid for adj2 in adjacent(adj)) == 2:
                new_grid.add(adj)
    grid = new_grid
print(f"Part two: {len(grid)}")
