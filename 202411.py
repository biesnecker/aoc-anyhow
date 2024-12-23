from functools import cache

from utils import input_as_string

input = list(map(int, input_as_string("202411.txt").split()))


@cache
def evolve(n: int, steps_left: int) -> int:
    if steps_left == 0:
        return 1  # the current number is the last one
    if n == 0:
        return evolve(1, steps_left - 1)
    ns = str(n)
    nsl = len(ns)
    if nsl % 2 == 0:
        first = int(ns[: nsl // 2])
        second = int(ns[nsl // 2 :])
        return evolve(first, steps_left - 1) + evolve(second, steps_left - 1)
    return evolve(n * 2024, steps_left - 1)


p_one = sum(evolve(n, 25) for n in input)
print(f"Part one: {p_one}")

p_two = sum(evolve(n, 75) for n in input)
print(f"Part two: {p_two}")
