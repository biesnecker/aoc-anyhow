DIGITS = "=-012"
SNAFU_BASE = len(DIGITS)
ZERO_OFFSET = DIGITS.index("0")


def snafu_to_int(snafu: str) -> int:
    num = 0
    for digit in snafu:
        num *= SNAFU_BASE
        num += DIGITS.index(digit) - ZERO_OFFSET
    return num


def int_to_snafu(num: int) -> str:
    snafu = ""
    while num:
        shifted_index = (num + ZERO_OFFSET) % SNAFU_BASE
        snafu += DIGITS[shifted_index]
        if shifted_index < ZERO_OFFSET:
            num += SNAFU_BASE
        num //= SNAFU_BASE
    return snafu[::-1]


total = 0
with open("202225.txt", "r") as f:
    for line in f:
        total += snafu_to_int(line.strip())
print(f"Part One: {int_to_snafu(total)}")
