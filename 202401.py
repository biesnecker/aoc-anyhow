from collections import Counter
from utils import input_as_list_of_numbers

left = []
right = []

for [a, b] in input_as_list_of_numbers("202401.txt"):
    left.append(a)
    right.append(b)

left.sort()
right.sort()

part_one = sum(abs(x - y) for (x, y) in zip(left, right))

print(f"Part one: {part_one}")

c = Counter(right)
part_two = sum(v * c[v] for v in left)

print(f"Part two: {part_two}")
