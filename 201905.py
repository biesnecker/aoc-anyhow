from intcode import (
    Intcode,
    IntcodeNeedsInput,
    IntcodeHasOutput,
    IntcodeHalted,
    intcode_from_file,
)

intcode = intcode_from_file("201905.txt")
part_one = 0
v = intcode.run()
while not isinstance(v, IntcodeHalted):
    if isinstance(v, IntcodeNeedsInput):
        v = v.continuation(1)
    elif isinstance(v, IntcodeHasOutput):
        part_one = v.value
        v = v.continuation()
    else:
        raise Exception("Unknown return value from intcode")

print(f"Part one: {part_one}")

intcode = intcode_from_file("201905.txt")
part_two = 0
v = intcode.run()
while not isinstance(v, IntcodeHalted):
    if isinstance(v, IntcodeNeedsInput):
        v = v.continuation(5)
    elif isinstance(v, IntcodeHasOutput):
        part_two = v.value
        v = v.continuation()
    else:
        raise Exception("Unknown return value from intcode")

print(f"Part two: {part_two}")
