def input_as_string(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def input_as_strings(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]


def input_as_numbers(filename):
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f]


def input_as_list_of_numbers(filename, split_on=None):
    with open(filename, "r") as f:
        return [
            [int(num.strip()) for num in line.strip().split(split_on)] for line in f
        ]
