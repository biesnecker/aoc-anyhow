import re

from utils import input_as_string

inp = input_as_string("202403.txt")

part_one = 0
matches = re.finditer(r"mul\((\d+),(\d+)\)", inp)
for match in matches:
    x = int(match.group(1))
    y = int(match.group(2))
    part_one += x * y

print(f"Part one: {part_one}")

part_two = 0
do = True
matches = re.finditer(r"mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)", inp)
for match in matches:
    if match.group(0) == "don't()":
        do = False
    elif match.group(0) == "do()":
        do = True
    else:
        if not do:
            continue
        x = int(match.group(1))
        y = int(match.group(2))
        part_two += x * y

print(f"Part two: {part_two}")
