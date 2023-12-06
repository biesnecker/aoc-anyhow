from enum import IntEnum


def read_intcode(filename):
    with open(filename, "r") as f:
        return [int(x) for x in f.read().split(",")]


def intcode_from_file(filename):
    return Intcode(read_intcode(filename))


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


class IntcodeNeedsInput:
    def __init__(self, continuation):
        assert callable(continuation)
        self.continuation = continuation


class IntcodeHasOutput:
    def __init__(self, value, continuation):
        self.value = value
        assert callable(continuation)
        self.continuation = continuation


class IntcodeHalted:
    pass


class Intcode:
    def __init__(self, program):
        self.program = program
        self.pointer = 0
        self.halted = False

    def run(self):
        while not self.halted:
            sv = self._step()
            if sv is not None:
                return sv

    def read(self, address):
        return self.program[address]

    def _step(self):
        (opcode, modes) = self._parse_opcode(self.program[self.pointer])
        self.pointer += 1
        if opcode == 99:
            self.halted = True
            return IntcodeHalted()
        elif opcode == 1:  # ADD
            a = self._read(modes[0])
            b = self._read(modes[1])
            self._write(a + b, modes[2])
        elif opcode == 2:  # MUL
            a = self._read(modes[0])
            b = self._read(modes[1])
            self._write(a * b, modes[2])
        elif opcode == 3:  # INPUT
            return self._input(modes)
        elif opcode == 4:  # OUTPUT
            return self._output(modes)
        elif opcode == 5:  # JUMP-IF-TRUE
            a = self._read(modes[0])
            b = self._read(modes[1])
            if a != 0:
                self.pointer = b
        elif opcode == 6:  # JUMP-IF-FALSE
            a = self._read(modes[0])
            b = self._read(modes[1])
            if a == 0:
                self.pointer = b
        elif opcode == 7:  # LESS-THAN
            a = self._read(modes[0])
            b = self._read(modes[1])
            self._write(1 if a < b else 0, modes[2])
        elif opcode == 8:  # EQUALS
            a = self._read(modes[0])
            b = self._read(modes[1])
            self._write(1 if a == b else 0, modes[2])
        else:
            raise ValueError(f"Invalid opcode: {opcode}")

    def _parse_opcode(self, opcode):
        o = opcode % 100
        p1 = (opcode // 100) % 10
        p2 = (opcode // 1000) % 10
        p3 = (opcode // 10000) % 10
        return (o, (p1, p2, p3))

    def _read(self, mode):
        if mode == ParameterMode.POSITION:
            x = self.program[self.program[self.pointer]]
        elif mode == ParameterMode.IMMEDIATE:
            x = self.program[self.pointer]
        else:
            raise ValueError(f"Invalid parameter mode: {mode}")
        self.pointer += 1
        return x

    def _write(self, value, mode):
        if mode == ParameterMode.POSITION:
            self.program[self.program[self.pointer]] = value
        elif mode == ParameterMode.IMMEDIATE:
            raise ValueError("Cannot write in immediate mode")
        else:
            raise ValueError(f"Invalid parameter mode: {mode}")
        self.pointer += 1

    # returns a function that takes an input value and continues execution
    # of the program
    def _input(self, modes):
        def f(value):
            self._write(value, modes[0])
            return self.run()

        return IntcodeNeedsInput(f)

    # returns a value and a function that continues execution of the program
    def _output(self, modes):
        value = self._read(modes[0])

        def f():
            return self.run()

        return IntcodeHasOutput(value, f)
