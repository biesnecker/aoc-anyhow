from intcode import OutputInterrupt, intcode_from_file

part_one = None
c = intcode_from_file("201909.txt", [1])
try:
    c.run()
except OutputInterrupt:
    part_one = c.output.popleft()
print(f"Part one: {part_one}")

part_two = None
c = intcode_from_file("201909.txt", [2])
try:
    c.run()
except OutputInterrupt:
    part_two = c.output.popleft()
print(f"Part two: {part_two}")
