from bisect import bisect_right
from operator import itemgetter

input = []
with open("202502.txt", "r") as f:
    ranges = f.readline().strip().split(",")
    input = sorted(
        map(lambda p: tuple(map(int, p.split("-"))), ranges),
        key=itemgetter(0),
    )


def generate_invalid(max_val: int) -> dict[int, bool]:
    invalid = dict()
    max_digits = len(str(max_val))

    for plen in range(1, max_digits + 1):
        max_reps = max_digits // plen
        start = max(1, 10 ** (plen - 1))
        for reps in range(2, max_reps + 1):
            for p in range(start, 10**plen):
                num = int(str(p) * reps)
                if num > max_val:
                    break
                if num not in invalid or not invalid[num]:
                    invalid[num] = reps == 2
    return invalid


# input must be sorted
def solve(input: list[tuple[int, int]]) -> tuple[int, int]:
    part_one = 0
    part_two = 0

    invalid = generate_invalid(input[-1][1])

    starts = [a for a, _ in input]
    for num, is_part_one in invalid.items():
        idx = bisect_right(starts, num) - 1
        if idx >= 0:
            a, b = input[idx]
            if a <= num <= b:
                part_two += num
                part_one += num if is_part_one else 0

    return part_one, part_two


solution = solve(input)
print(solution[0])
print(solution[1])
