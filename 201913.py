from collections import defaultdict
from enum import IntEnum
from intcode import Intcode, InputInterrupt, OutputInterrupt, intcode_from_file


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


screen = defaultdict(lambda: Tile.EMPTY)

game = intcode_from_file("201913.txt")
out = []
while not game.halted:
    try:
        game.run()
    except OutputInterrupt:
        out.append(game.output.popleft())
        match out:
            case [x, y, tile]:
                screen[(x, y)] = Tile(tile)
                out.clear()
print(f"Part one: {sum(1 for tile in screen.values() if tile == Tile.BLOCK)}")

game = intcode_from_file("201913.txt", mod={0: 2})
out = []
score = 0
ball_x = 0
paddle_x = 0

while not game.halted:
    try:
        game.run()
    except OutputInterrupt:
        out.append(game.pop_output())
        match out:
            case [-1, 0, tile]:
                score = tile
                out.clear()
            case [x, _, Tile.PADDLE]:
                paddle_x = x
                out.clear()
            case [x, _, Tile.BALL]:
                ball_x = x
                out.clear()
            case [_, _, _]:
                out.clear()
    except InputInterrupt:
        game.append_input(-1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0)
print(f"Part two: {score}")
