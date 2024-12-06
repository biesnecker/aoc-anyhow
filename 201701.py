from utils import input_as_string

part_one = 0
part_two = 0

inp = input_as_string("201701.txt")
half = len(inp) // 2

for idx, d in enumerate(inp):
    part_one_idx = (idx + 1) % len(inp)
    part_two_idx = (idx + half) % len(inp)
    if d == inp[part_one_idx]:
        part_one += int(d)
    if d == inp[part_two_idx]:
        part_two += int(d)

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
