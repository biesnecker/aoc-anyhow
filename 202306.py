import math

with open("202306.txt", "r") as f:
    data = f.read().splitlines()
    times = [int(x) for x in data[0].split(": ")[1].split()]
    dists = [int(x) for x in data[1].split(": ")[1].split()]


def find_bounds(time, dist):
    a = -1
    b = time
    c = -dist

    discriminant = b**2 - 4 * a * c
    assert discriminant >= 0

    x1 = (-b + math.sqrt(discriminant)) / (2 * a)
    x2 = (-b - math.sqrt(discriminant)) / (2 * a)
    lower_bound, upper_bound = sorted([x1, x2])
    lower_bound = math.ceil(max(lower_bound, 0))
    upper_bound = math.floor(min(upper_bound, time))
    return lower_bound, upper_bound


part_one = []
for time, dist in zip(times, dists):
    lb, ub = find_bounds(time, dist)
    part_one.append(ub - lb + 1)
print(f"Part one: {math.prod(part_one)}")


part_two = 0
time = int("".join(map(str, times)))
dist = int("".join(map(str, dists)))
lb, ub = find_bounds(time, dist)
part_two = ub - lb + 1
print(f"Part two: {part_two}")
