"""Writes 16-byte big-endian records into a byte list, then decodes every record again and again."""
import sys
import time


def append_integer_big_endian(records, value):
    bits = value & 0xFFFFFFFF
    records.append((bits >> 24) & 0xFF)
    records.append((bits >> 16) & 0xFF)
    records.append((bits >> 8) & 0xFF)
    records.append(bits & 0xFF)


def append_short_big_endian(records, value):
    bits = value & 0xFFFF
    records.append((bits >> 8) & 0xFF)
    records.append(bits & 0xFF)


def read_integer_big_endian(records, position):
    bits = (records[position] << 24) | (records[position + 1] << 16) | (records[position + 2] << 8) | records[position + 3]
    return bits - 0x100000000 if bits >= 0x80000000 else bits


def read_short_big_endian(records, position):
    bits = (records[position] << 8) | records[position + 1]
    return bits - 0x10000 if bits >= 0x8000 else bits


def decode(records):
    total = 0
    position = 0
    while position + 15 < len(records):
        identity = read_integer_big_endian(records, position)
        across = read_integer_big_endian(records, position + 4)
        down = read_integer_big_endian(records, position + 8)
        kind = read_short_big_endian(records, position + 12)
        flags = read_short_big_endian(records, position + 14)
        total = total + identity + across + down * kind + flags
        position = position + 16
    return total


def rounds(records):
    total = 0
    for round_number in range(300):
        total = total + decode(records) + round_number
    return total


def main():
    records = []
    for index in range(100000):
        append_integer_big_endian(records, index)
        append_integer_big_endian(records, index * 7 - 50000)
        append_integer_big_endian(records, index % 1000)
        append_short_big_endian(records, index % 5)
        append_short_big_endian(records, index % 3)
    start = time.perf_counter_ns()
    total = rounds(records)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
