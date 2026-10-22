"""Hashes a class's schema text on every header check and counts the headers that match the reader's schema."""
import struct
import sys
import time


class Reading:
    def __init__(self, sensor, level, label):
        self.sensor = sensor
        self.level = level
        self.label = label


class ClassDescription:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


reading_class = ClassDescription("Reading", [("sensor", "Integer"), ("level", "Float"), ("label", "String")])


class Writer:
    def __init__(self, described):
        self.described = described


class Reader:
    def __init__(self, described):
        self.described = described


def schema_of(described):
    text = described.name + "{"
    for index, (name, kind) in enumerate(described.attributes):
        if index > 0:
            text += ";"
        text += name + ":" + kind
    text += "}"
    value = 14695981039346656037
    for byte in text.encode():
        value = ((value ^ byte) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    if value >= 1 << 63:
        value -= 1 << 64
    return value


def writer_schema(writer):
    return schema_of(writer.described)


def reader_schema(reader):
    return schema_of(reader.described)


def received_headers(writer, count):
    headers = []
    for index in range(count):
        header = writer_schema(writer)
        if index % 10 == 0:
            header = index
        headers.append(header)
    return headers


def is_current(reader, header):
    return header == reader_schema(reader)


def count_current(reader, headers):
    count = 0
    for header in headers:
        if is_current(reader, header):
            count += 1
    return count


def write_reading(reading):
    label = reading.label.encode()
    return struct.pack("<ifi", reading.sensor, reading.level, len(label)) + label


def read_reading(data):
    if len(data) < 12:
        return None
    sensor, level, length = struct.unpack("<ifi", data[:12])
    if length < 0 or length != len(data) - 12:
        return None
    return Reading(sensor, level, data[12:].decode())


def sent_and_read_back(sensor):
    reading = Reading(sensor, 0.0, "")
    read = read_reading(write_reading(reading))
    if read is None:
        raise SystemExit(1)
    return read.sensor


def main():
    writer = Writer(reading_class)
    reader = Reader(reading_class)
    start = time.perf_counter_ns()
    headers = received_headers(writer, 200000)
    accepted = 0
    for _ in range(10):
        accepted += count_current(reader, headers)
    microseconds = (time.perf_counter_ns() - start) // 1000
    sensor = sent_and_read_back(7)
    print(f"accepted {accepted} sensor {sensor}")
    print(f"schema {writer_schema(writer)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
