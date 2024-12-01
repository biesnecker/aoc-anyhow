from intcode import intcode_from_prog, OutputInterrupt, read_intcode

prog = read_intcode("201919.txt")


def check(x, y):
    c = intcode_from_prog(prog)
    c.input.extend([x, y])
    try:
        c.run()
    except OutputInterrupt:
        return c.pop_output() == 1
    raise Exception("Shouldn't get here")


affected = sum(check(x, y) for x in range(50) for y in range(50))

print(f"Part one: {affected}")

x = y = 0
while not check(x + 99, y):
    y += 1
    while not check(x, y + 99):
        x += 1
print(f"Part two: {x*10000 + y}")
