from intcode import Intcode, read_intcode

prog = read_intcode("201902.txt")
prog[1] = 12
prog[2] = 2

intcode = Intcode(prog)
intcode.run()

print(f"Part one: {intcode.read(0)}")

for noun in range(100):
    for verb in range(100):
        prog = read_intcode("201902.txt")
        prog[1] = noun
        prog[2] = verb

        intcode = Intcode(prog)
        intcode.run()

        if intcode.read(0) == 19690720:
            print(f"Part two: {100 * noun + verb}")
            break
