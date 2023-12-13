first_basement = None

with open("201501.txt", "r") as f:
    floor = 0
    for i, c in enumerate(f.readline().strip()):
        if c == "(":
            floor += 1
        else:
            floor -= 1
            if floor == -1 and first_basement is None:
                first_basement = i + 1
print(f"Part one: {floor}")
print(f"Part two: {first_basement}")
