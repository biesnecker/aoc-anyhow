from collections import Counter

left = []
right = []

with open("202401.txt", "r") as f:
    for line in f:
        [a, b] = line.split()
        left.append(int(a))
        right.append(int(b))

    left.sort()
    right.sort()

part_one = 0

for i in range(len(left)):
    part_one += abs(right[i] - left[i])

print(f"Part one: {part_one}")

part_two = 0
c = Counter(right)

for v in left:
    part_two += c[v] * v

print(f"Part two: {part_two}")
