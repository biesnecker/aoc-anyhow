from collections import defaultdict

nums = []
symbols = {}

with open("202303.txt", "r") as f:
    for y, line in enumerate(f):
        current = None
        start_x = None
        end_x = None
        for x, c in enumerate(line.strip()):
            if c.isdigit():
                if current is None:
                    current = int(c)
                    start_x = x
                    end_x = x
                else:
                    current = current * 10 + int(c)
                    end_x = x
            else:
                if current is not None:
                    nums.append((current, start_x, end_x, y))
                    current = None
                    start_x = None
                    end_x = None
                if c != ".":
                    symbols[(x, y)] = c
        if current is not None:
            nums.append((current, start_x, end_x, y))


def get_adjacent(start_x, end_x, y):
    for yp in range(y - 1, y + 2):
        for x in range(start_x - 1, end_x + 2):
            if yp == y and x >= start_x and x <= end_x:
                continue
            if (x, yp) in symbols:
                yield (symbols[(x, yp)], x, yp)


def has_adjacent(start_x, end_x, y):
    return any(True for _ in get_adjacent(start_x, end_x, y))


part_one = 0
for num, start_x, end_x, y in nums:
    if has_adjacent(start_x, end_x, y):
        part_one += num
print(f"Part one: {part_one}")

part_two = 0
star_adjacent = defaultdict(list)

for num, start_x, end_x, y in nums:
    for sym, x, y in get_adjacent(start_x, end_x, y):
        if sym == "*":
            star_adjacent[(x, y)].append(num)

for nums in star_adjacent.values():
    if len(nums) == 2:
        part_two += nums[0] * nums[1]
print(f"Part two: {part_two}")
