import pickle
from collections import defaultdict, deque
from collections.abc import Sequence
from enum import IntEnum


def read_intcode(filename):
    with open(filename, "r") as f:
        return [int(x) for x in f.read().split(",")]


def intcode_from_file(filename, input=deque(), *, mod={}):
    return Intcode(read_intcode(filename), input, mod=mod)


def intcode_from_prog(prog, input=deque(), *, mod={}):
    return Intcode(prog.copy(), input, mod=mod)


def intcode_from_pickle(bytes):
    return pickle.loads(bytes)


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    JIT = 5
    JIF = 6
    LT = 7
    EQ = 8
    REL = 9
    HALT = 99


class InputInterrupt(Exception):
    pass


class OutputInterrupt(Exception):
    pass


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Intcode:
    def __init__(self, program, input=deque(), *, mod={}):
        self.program = program
        self.pointer = 0
        self.base = 0
        self.halted = False
        self.memory = defaultdict(int)
        assert isinstance(input, Sequence)
        self.input = deque(input)
        self.output = deque()
        if mod:
            for k, v in mod.items():
                self.program[k] = v

    def __copy__(self):
        c = Intcode(
            self.program.copy(),
            self.input.copy(),
        )
        c.pointer = self.pointer
        c.base = self.base
        c.halted = self.halted
        c.memory = self.memory.copy()
        c.output = self.output.copy()
        return c

    def append_input(self, value):
        self.input.append(value)

    def pop_output(self):
        return self.output.popleft()

    def pickle(self):
        return pickle.dumps(self)

    def run(self):
        while not self.halted:
            match self._parse_opcode(self.program[self.pointer]):
                case (Opcode.HALT, _):
                    self.halted = True
                    return
                case (Opcode.ADD, (m1, m2, m3)):
                    a = self._read(self.pointer + 1, m1)
                    b = self._read(self.pointer + 2, m2)
                    self._write(self.pointer + 3, a + b, m3)
                    self.pointer += 4
                case (Opcode.MUL, (m1, m2, m3)):
                    a = self._read(self.pointer + 1, m1)
                    b = self._read(self.pointer + 2, m2)
                    self._write(self.pointer + 3, a * b, m3)
                    self.pointer += 4
                case (Opcode.IN, (m1, _, _)):
                    if not self.input:
                        raise InputInterrupt()
                    v = self.input.popleft()
                    self._write(self.pointer + 1, v, m1)
                    self.pointer += 2
                case (Opcode.OUT, (m1, _, _)):
                    v = self._read(self.pointer + 1, m1)
                    self.output.append(v)
                    self.pointer += 2
                    raise OutputInterrupt()
                case (Opcode.JIT, (m1, m2, _)):
                    v = self._read(self.pointer + 1, m1)
                    if v != 0:
                        self.pointer = self._read(self.pointer + 2, m2)
                    else:
                        self.pointer += 3
                case (Opcode.JIF, (m1, m2, _)):
                    v = self._read(self.pointer + 1, m1)
                    if v == 0:
                        self.pointer = self._read(self.pointer + 2, m2)
                    else:
                        self.pointer += 3
                case (Opcode.LT, (m1, m2, m3)):
                    a = self._read(self.pointer + 1, m1)
                    b = self._read(self.pointer + 2, m2)
                    self._write(self.pointer + 3, 1 if a < b else 0, m3)
                    self.pointer += 4
                case (Opcode.EQ, (m1, m2, m3)):
                    a = self._read(self.pointer + 1, m1)
                    b = self._read(self.pointer + 2, m2)
                    self._write(self.pointer + 3, 1 if a == b else 0, m3)
                    self.pointer += 4
                case (Opcode.REL, (m1, _, _)):
                    self.base += self._read(self.pointer + 1, m1)
                    self.pointer += 2
                case opcode:
                    raise Exception(
                        f"Unknown opcode: {opcode} (raw: {self.program[self.pointer]}) @ position {self.pointer}"
                    )

    def _parse_opcode(self, opcode):
        o = opcode % 100
        p1 = (opcode // 100) % 10
        p2 = (opcode // 1000) % 10
        p3 = (opcode // 10000) % 10
        return (o, (p1, p2, p3))

    def _read(self, address, mode):
        if mode == ParameterMode.POSITION:
            return self._read_memory(self._read_memory(address))
        elif mode == ParameterMode.IMMEDIATE:
            return self._read_memory(address)
        elif mode == ParameterMode.RELATIVE:
            return self._read_memory(self.base + self._read_memory(address))
        else:
            raise Exception(f"Unknown parameter mode: {mode}")

    def _read_memory(self, address):
        if address < 0:
            raise Exception(f"Negative memory address: {address}")
        elif address >= len(self.program):
            return self.memory[address]
        else:
            return self.program[address]

    def _write(self, address, value, mode):
        if mode == ParameterMode.POSITION:
            self._write_memory(self._read_memory(address), value)
        elif mode == ParameterMode.IMMEDIATE:
            raise Exception("Cannot write to immediate parameter")
        elif mode == ParameterMode.RELATIVE:
            self._write_memory(self.base + self._read_memory(address), value)
        else:
            raise Exception(f"Unknown parameter mode: {mode}")

    def _write_memory(self, address, value):
        if address < 0:
            raise Exception(f"Negative memory address: {address}")
        elif address >= len(self.program):
            self.memory[address] = value
        else:
            self.program[address] = value
