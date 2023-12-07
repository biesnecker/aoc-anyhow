from intcode import Intcode, OutputInterrupt, intcode_from_file

intcode = intcode_from_file("201905.txt", [1])
while not intcode.halted:
    try:
        intcode.run()
    except OutputInterrupt:
        pass  # only need the last output

print(f"Part one: {intcode.output[-1]}")

intcode = intcode_from_file("201905.txt", [5])
part_two = 0
try:
    v = intcode.run()
except OutputInterrupt:
    part_two = intcode.output.popleft()

print(f"Part two: {part_two}")
