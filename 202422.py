from collections import deque
from typing import Iterator

from utils import input_as_numbers

codes = input_as_numbers("202422.txt")


def step(code: int) -> int:
    code ^= code << 6
    code &= 16777215
    code ^= code >> 5
    code &= 16777215
    code ^= code << 11
    return code & 16777215


def step_code(code: int, steps: int = 2000) -> Iterator[int]:
    yield code
    for _ in range(steps):
        code = step(code)
        yield code


def last_code(code: int, steps: int = 2000) -> int:
    return deque(step_code(code, steps), maxlen=1).pop()


part_one = sum(last_code(c, steps=2000) for c in codes)
print(f"Part one: {part_one}")
