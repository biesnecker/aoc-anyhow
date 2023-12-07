from intcode import Intcode, intcode_from_file

intcode = intcode_from_file("201902.txt", mod={1: 12, 2: 2})
intcode.run()

print(f"Part one: {intcode.program[0]}")

for noun in range(100):
    for verb in range(100):
        intcode = intcode_from_file("201902.txt", mod={1: noun, 2: verb})
        intcode.run()

        if intcode.program[0] == 19690720:
            print(f"Part two: {100 * noun + verb}")
            break
