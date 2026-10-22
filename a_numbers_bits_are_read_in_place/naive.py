"""Round-trips floats through half precision by reading and building their bit patterns."""
import struct
import sys
import time

FLOAT = struct.Struct("<f")
BITS = struct.Struct("<I")


def float_bits(value):
    return BITS.unpack(FLOAT.pack(value))[0]


def bits_as_float(bits):
    return FLOAT.unpack(BITS.pack(bits))[0]


def to_half_precision(value):
    bit_pattern = float_bits(value)
    sign_part = (bit_pattern >> 16) & 32768
    magnitude = bit_pattern & 2147483647
    if magnitude >= 1199570944:
        half = 31744
        if magnitude > 2139095040:
            half = 32256
    elif magnitude < 947912704:
        magic = 1056964608
        shifted = bits_as_float(magnitude) + bits_as_float(magic)
        half = (float_bits(shifted) - magic) & 0xFFFFFFFF
    else:
        odd = (magnitude >> 13) & 1
        rounded = (magnitude + 3355447295 + odd) & 0xFFFFFFFF
        half = rounded >> 13
    return (half | sign_part) & 0xFFFF


def half_precision_to_float(half):
    shifted_exponent = 260046848
    bit_pattern = (half & 32767) << 13
    exponent = shifted_exponent & bit_pattern
    bit_pattern = (bit_pattern + 939524096) & 0xFFFFFFFF
    if exponent == shifted_exponent:
        bit_pattern = (bit_pattern + 939524096) & 0xFFFFFFFF
    elif exponent == 0:
        bit_pattern = (bit_pattern + 8388608) & 0xFFFFFFFF
        magic = 947912704
        value = bits_as_float(bit_pattern) - bits_as_float(magic)
        bit_pattern = float_bits(value)
    sign_part = (half & 32768) << 16
    bit_pattern = bit_pattern | sign_part
    return bits_as_float(bit_pattern)


def round_trips(count):
    total = 0
    for index in range(count):
        value = float(index % 160000 - 20000)
        value = value * 0.5
        half = to_half_precision(value)
        back = half_precision_to_float(half)
        back_bits = float_bits(back)
        total = total + half + back_bits
    return total


def main():
    start = time.perf_counter_ns()
    total = round_trips(30000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
