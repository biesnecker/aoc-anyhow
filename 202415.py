from utils import input_as_strings_iter, Dir, xy_to_coord, coord_to_xy
from typing import Dict, List, Tuple


def parse_input(
    part_two=False,
) -> Tuple[Dict[complex, str], List[Dir], complex, int, int]:
    grid: Dict[complex, str] = {}
    max_x = max_y = 0
    moves: List[Dir] = []
    input_part_one = True
    start_pos = 0
    for y, line in enumerate(input_as_strings_iter("202415.txt")):
        if line == "":
            input_part_one = False
            continue
        if input_part_one:
            max_y = y
            for x, c in enumerate(line):
                if part_two:
                    max_x = 2 * x + 1
                    coord = xy_to_coord(2 * x)
                    if c == "@":
                        start_pos = coord
                        c = "."
                    if c == "#":
                        grid[coord] = c
                        grid[coord + Dir.EAST.value] = c
                    elif c == ".":
                        grid[coord] = c
                        grid[coord + Dir.EAST.value] = c
                    elif c == "O":
                        grid[coord] = "["
                        grid[coord + Dir.EAST.value] = "]"
                    else:
                        raise ValueError(f"Unknown character {c}")
                else:
                    max_x = max(max_x, x)
                    coord = xy_to_coord(x, y)
                    if c == "@":
                        start_pos = coord
                        c = "."
                    grid[coord] = c
        else:
            for c in line:
                match c:
                    case "^":
                        moves.append(Dir.NORTH)
                    case "v":
                        moves.append(Dir.SOUTH)
                    case "<":
                        moves.append(Dir.WEST)
                    case ">":
                        moves.append(Dir.EAST)
                    case _:
                        raise ValueError(f"Unknown character {c}")
    assert start_pos != 0
    return grid, moves, start_pos, max_x, max_y


def display(grid: Dict[complex, str], pos: complex, max_x: int, max_y: int) -> None:
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if pos == xy_to_coord(x, y):
                print("@", end="")
            else:
                print(grid[xy_to_coord(x, y)], end="")
        print()
    print()


grid, moves, pos, max_x, max_y = parse_input()

for move in moves:
    # display(grid, pos, max_x, max_y)
    if grid[pos + move.value] == ".":
        pos += move.value
        continue
    elif grid[pos + move.value] == "#":
        continue

    assert grid[pos + move.value] == "O"
    # We need to move boxes. We can move multiple boxes at once,
    # but only if there's an empty cell somewhere along the line
    # of movement before we hit a wall.
    to_move = []
    bpos = pos + move.value
    has_space = False
    while True:
        if grid[bpos] == "O":
            to_move.append(bpos)
            bpos += move.value
        elif grid[bpos] == "#":
            break
        else:
            has_space = True
            break
    if not has_space:
        # There was no space so we can't move the boxes
        continue
    for bpos in to_move:
        grid[bpos + move.value] = "O"
    pos += move.value
    grid[pos] = "."


part_one = 0
for loc, c in grid.items():
    if c != "O":
        continue
    x, y = coord_to_xy(loc)
    part_one += 100 * y + x
print(f"Part one: {part_one}")
