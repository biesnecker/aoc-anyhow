# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy",
#     "scipy",
# ]
# ///

from collections import defaultdict
from functools import reduce
from itertools import combinations
from operator import xor

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

targets: dict[int, int] = {}
buttons: defaultdict[int, list[list[int]]] = defaultdict(list)
button_masks: defaultdict[int, list[int]] = defaultdict(list)
joltages: dict[int, list[int]] = {}

with open("202510.txt", "r") as f:
    for i, line in enumerate(f.readlines()):
        for part in line.strip().split(" "):
            if part[0] == "[":
                targets[i] = int(
                    part[1:-1].replace(".", "0").replace("#", "1")[::-1], base=2
                )
            elif part[0] == "(":
                bl = list(map(int, part[1:-1].split(",")))
                buttons[i].append(bl)
                button_masks[i].append(
                    reduce(lambda a, b: a | b, map(lambda n: 1 << n, bl))
                )
            else:
                joltages[i] = list(map(int, part[1:-1].split(",")))


def part_one(target: int, button_masks: list[int]) -> int:
    n = len(button_masks)
    for num_presses in range(n + 1):
        for combo in combinations(range(n), num_presses):
            if reduce(xor, (button_masks[i] for i in combo), 0) == target:
                return num_presses
    raise Exception("No solution!")


def part_two(buttons: list[list[int]], joltages: list[int]) -> int:
    n_buttons = len(buttons)
    n_counters = len(joltages)

    # Build constraint matrix A where A[j][i] = 1 if button i affects counter j
    A = np.zeros((n_counters, n_buttons))
    for i, btn in enumerate(buttons):
        for j in btn:
            A[j][i] = 1

    # Objective: minimize sum of button presses
    c = np.ones(n_buttons)

    # Constraints: A @ x == joltages (equality constraint)
    constraints = LinearConstraint(A, joltages, joltages)

    # Bounds: x >= 0, upper bound generous enough
    max_val = max(joltages) if joltages else 0
    bounds = Bounds(lb=0, ub=max_val + 1)

    # All variables must be integers
    integrality = np.ones(n_buttons)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        raise Exception(f"No solution found: {result.message}")


print(sum(part_one(targets[i], button_masks[i]) for i in range(len(targets))))
print(sum(part_two(buttons[i], joltages[i]) for i in range(len(targets))))
