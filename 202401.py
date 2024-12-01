from collections import Counter

left = []
right = []

with open("202401.txt", "r") as f:
    for line in f:
        [a, b] = list(map(int, line.split()))
        left.append(a)
        right.append(b)

    left.sort()
    right.sort()

part_one = sum(abs(x - y) for (x, y) in zip(left, right))

print(f"Part one: {part_one}")

c = Counter(right)
part_two = sum(v * c[v] for v in left)

print(f"Part two: {part_two}")
