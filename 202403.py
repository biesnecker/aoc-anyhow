import re

from utils import input_as_string

inp = input_as_string("202403.txt")

part_one = 0
part_two = 0
do = True
for match in re.finditer(r"mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)", inp):
    if match.group(0) == "don't()":
        do = False
    elif match.group(0) == "do()":
        do = True
    else:
        x = int(match.group(1))
        y = int(match.group(2))
        res = x * y
        part_one += res
        if do:
            part_two += res

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
