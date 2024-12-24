import math
from abc import abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass
class Signal:
    src: str
    dest: str
    value: bool


class Box:
    def __init__(self, label, outputs):
        self.label = label
        self.outputs = outputs

    @abstractmethod
    def handle_input(self, input):
        pass

    def set_inputs(self, inputs):
        pass


class Broadcast(Box):
    def handle_input(self, input):
        # print(f"Broadcast {self.label} got {input.value} from {input.src}")
        for output in self.outputs:
            yield Signal(self.label, output, input.value)


class FlipFlop(Box):
    def __init__(self, label, outputs):
        super().__init__(label, outputs)
        self.state = False

    def handle_input(self, input):
        # print(f"Flipflop {self.label} got {input.value} from {input.src}")
        if not input.value:  # low signal
            s = False
            if self.state:  # it was already on
                self.state = False
            else:  # it was off
                self.state = True
                s = True
            for output in self.outputs:
                yield Signal(self.label, output, s)


class Conj(Box):
    def __init__(self, label, outputs):
        super().__init__(label, outputs)
        self.state = None

    def handle_input(self, input):
        # print(f"Conj {self.label} got {input.value} from {input.src}")
        self.state[input.src] = input.value
        s = not all(self.state.values())
        for output in self.outputs:
            yield Signal(self.label, output, s)

    def set_inputs(self, inputs):
        self.state = {input: False for input in inputs}


def get_network():
    network = {}
    input_map = defaultdict(list)
    with open("202320.txt", "r") as f:
        for line in f:
            [label_raw, outputs_raw] = line.strip().split(" -> ")
            outputs = outputs_raw.split(", ")
            (type, label) = (
                None if label_raw == "broadcaster" else label_raw[0],
                "broadcaster" if label_raw == "broadcaster" else label_raw[1:],
            )
            match (type, label):
                case (_, "broadcaster"):
                    network[label] = Broadcast(label, outputs)
                case ("%", label):
                    network[label] = FlipFlop(label, outputs)
                case ("&", label):
                    network[label] = Conj(label, outputs)
                case _:
                    raise ValueError(f"Unknown label type: {label_raw}")
            for output in outputs:
                input_map[output].append(label)
    for dest, srcs in input_map.items():
        if dest in network:
            network[dest].set_inputs(srcs)
    return network


def push_button(n, *, target=None):
    low_count, high_count, target_sent_high = 0, 0, False
    q = deque([Signal(None, "broadcaster", False)])
    while q:
        signal = q.popleft()
        if signal.value:
            high_count += 1
        else:
            low_count += 1
        if target is not None and signal.src == target and signal.value:
            assert not target_sent_high
            target_sent_high = True
        if signal.dest in n:
            q.extend(n[signal.dest].handle_input(signal))
    return (low_count, high_count, target_sent_high)


p1low, p1high = 0, 0
network = get_network()
for _ in range(1000):
    (low, high, _) = push_button(network)
    p1low += low
    p1high += high
print(f"Part one: {p1low*p1high}")


def first_high(target):
    i = 1
    network = get_network()
    while True:
        (_, _, high) = push_button(network, target=target)
        if high:
            break
        i += 1
    return i


part_two = []
for t in ["qz", "cq", "jx", "tt"]:  # maybe input specific?
    res = first_high(t)
    part_two.append(res)
print(f"Part two: {math.lcm(*part_two)}")
