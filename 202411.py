from utils import input_as_string
from functools import cache

input = list(map(int, input_as_string("202411.txt").split()))


@cache
def evolve(n: int, steps_left: int) -> int:
    if steps_left == 0:
        return 1  # the current number is the last one
    if n == 0:
        return evolve(1, steps_left - 1)
    if len(str(n)) % 2 == 0:
        first = int(str(n)[: len(str(n)) // 2])
        second = int(str(n)[len(str(n)) // 2 :])
        return evolve(first, steps_left - 1) + evolve(second, steps_left - 1)
    return evolve(n * 2024, steps_left - 1)


p_one = sum(evolve(n, 25) for n in input)
print(f"Part one: {p_one}")

p_two = sum(evolve(n, 75) for n in input)
print(f"Part two: {p_two}")
