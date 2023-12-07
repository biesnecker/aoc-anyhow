from intcode import Intcode, InputInterrupt, OutputInterrupt, read_intcode
from itertools import permutations

prog = read_intcode("201907.txt")
part_one = 0
for phase in permutations(range(5)):
    signal = 0
    for p in phase:
        intcode = Intcode(prog.copy(), [p, signal])
        try:
            signal = intcode.run()
        except OutputInterrupt:
            signal = intcode.output.popleft()
    part_one = max(part_one, signal)
print(f"Part one: {part_one}")

part_two = 0
for phase in permutations(range(5, 10)):
    amps = [Intcode(prog.copy(), [p]) for p in phase]
    amps[0].append_input(0)  # provide initial input to first amp
    all_halted = False
    while not all_halted:
        all_halted = True
        for i, amp in enumerate(amps):
            all_halted &= amp.halted
            try:
                amp.run()
            except InputInterrupt:
                pass
            except OutputInterrupt:
                amps[(i + 1) % 5].append_input(amp.pop_output())
    # last output of last amp was sent to the input of the first amp
    part_two = max(part_two, amps[0].input[-1])
print(f"Part two: {part_two}")
