with open("201502.txt", "r") as f:
    dims = [tuple(map(int, line.split("x"))) for line in f]

part_one = sum(
    2 * (l * w + w * h + h * l) + min(l * w, w * h, h * l) for l, w, h in dims
)
print(f"Part one: {part_one}")

part_two = sum(min(l + w, w + h, h + l) * 2 + l * w * h for l, w, h in dims)
print(f"Part two: {part_two}")
