"""Renders three voices of three classes behind one method, each in turn on the one thread."""
import sys
import time


class Voice:
    def __init__(self):
        self.level = 0
        self.phase = 0

    def render(self):
        raise NotImplementedError


class Sine(Voice):
    def render(self):
        for sample in range(30000000):
            self.phase = (self.phase + 7) % 1000
            folded = self.phase
            if folded > 500:
                folded = 1000 - folded
            self.level = self.level + folded


class Square(Voice):
    def render(self):
        for sample in range(30000000):
            self.phase = (self.phase + 11) % 1000
            if self.phase < 500:
                self.level = self.level + 3
            else:
                self.level = self.level + 1


class Saw(Voice):
    def render(self):
        for sample in range(30000000):
            self.phase = (self.phase + 13) % 1000
            self.level = self.level + self.phase % 97


def main():
    voices = [Sine(), Square(), Saw()]
    start = time.perf_counter_ns()
    for voice in voices:
        voice.render()
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"{voices[0].level} {voices[1].level} {voices[2].level}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
