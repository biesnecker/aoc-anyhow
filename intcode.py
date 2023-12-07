from enum import IntEnum
from collections import deque


def read_intcode(filename):
    with open(filename, "r") as f:
        return [int(x) for x in f.read().split(",")]


def intcode_from_file(filename, input=lambda: deque()):
    return Intcode(read_intcode(filename), input)


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    JIT = 5
    JIF = 6
    LT = 7
    EQ = 8
    HALT = 99


class InputInterrupt(Exception):
    pass


class OutputInterrupt(Exception):
    pass


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


class Intcode:
    def __init__(self, program, input=lambda: deque()):
        self.program = program
        self.pointer = 0
        self.halted = False
        self.input = input
        self.output = deque()

    def append_input(self, value):
        self.input.append(value)

    def pop_output(self):
        return self.output.popleft()

    def run(self):
        while not self.halted:
            opcode, modes = self._parse_opcode(self.program[self.pointer])
            if opcode == Opcode.HALT:
                self.halted = True
                return
            elif opcode == Opcode.ADD:
                a = self._read(self.pointer + 1, modes[0])
                b = self._read(self.pointer + 2, modes[1])
                self._write(self.pointer + 3, a + b, modes[2])
                self.pointer += 4
            elif opcode == Opcode.MUL:
                a = self._read(self.pointer + 1, modes[0])
                b = self._read(self.pointer + 2, modes[1])
                self._write(self.pointer + 3, a * b, modes[2])
                self.pointer += 4
            elif opcode == Opcode.IN:
                try:
                    v = self.input.popleft()
                    self._write(self.pointer + 1, v, modes[0])
                    self.pointer += 2
                except IndexError:
                    raise InputInterrupt()
            elif opcode == Opcode.OUT:
                v = self._read(self.pointer + 1, modes[0])
                self.output.append(v)
                self.pointer += 2
                raise OutputInterrupt()
            elif opcode == Opcode.JIT:
                v = self._read(self.pointer + 1, modes[0])
                if v != 0:
                    self.pointer = self._read(self.pointer + 2, modes[1])
                else:
                    self.pointer += 3
            elif opcode == Opcode.JIF:
                v = self._read(self.pointer + 1, modes[0])
                if v == 0:
                    self.pointer = self._read(self.pointer + 2, modes[1])
                else:
                    self.pointer += 3
            elif opcode == Opcode.LT:
                a = self._read(self.pointer + 1, modes[0])
                b = self._read(self.pointer + 2, modes[1])
                self._write(self.pointer + 3, 1 if a < b else 0, modes[2])
                self.pointer += 4
            elif opcode == Opcode.EQ:
                a = self._read(self.pointer + 1, modes[0])
                b = self._read(self.pointer + 2, modes[1])
                self._write(self.pointer + 3, 1 if a == b else 0, modes[2])
                self.pointer += 4
            else:
                raise Exception(f"Unknown opcode: {opcode} @ position {self.pointer}")

    def _parse_opcode(self, opcode):
        o = opcode % 100
        p1 = (opcode // 100) % 10
        p2 = (opcode // 1000) % 10
        p3 = (opcode // 10000) % 10
        return (o, (p1, p2, p3))

    def _read(self, address, mode):
        if mode == ParameterMode.POSITION:
            return self.program[self.program[address]]
        elif mode == ParameterMode.IMMEDIATE:
            return self.program[address]
        else:
            raise Exception(f"Unknown parameter mode: {mode}")

    def _write(self, address, value, mode):
        if mode == ParameterMode.POSITION:
            self.program[self.program[address]] = value
        elif mode == ParameterMode.IMMEDIATE:
            raise Exception("Cannot write to immediate parameter")
        else:
            raise Exception(f"Unknown parameter mode: {mode}")
