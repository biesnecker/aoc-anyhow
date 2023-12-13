import hashlib

prefix = b"yzbqklnj"


def md5(s):
    return hashlib.md5(s).hexdigest()


def with_leading_zeros(prefix, n):
    for i in range(100000, 100000000):
        if md5(prefix + bytes(str(i), "ascii"))[:n] == "0" * n:
            return i


print(f"Part one: {with_leading_zeros(prefix, 5)}")
print(f"Part two: {with_leading_zeros(prefix, 6)}")
