"""Renders a drum track and a bass track, each with a meter of its own that records its samples."""
import sys
import time


class Meter:
    def __init__(self):
        self.total = 0
        self.peak = 0
        self.loud = []

    def record(self, sample):
        self.total = self.total + sample
        if sample > self.peak:
            self.peak = sample
        if sample > 995:
            self.loud.append(sample)


class Track:
    def __init__(self):
        self.meter = Meter()
        self.phase = 0

    def render(self):
        raise NotImplementedError


class Drum(Track):
    def render(self):
        for _ in range(20000000):
            self.phase = (self.phase + 7) % 1000
            self.meter.record(self.phase)


class Bass(Track):
    def render(self):
        for _ in range(20000000):
            self.phase = (self.phase + 13) % 1000
            folded = self.phase
            if folded > 500:
                folded = 1000 - folded
            self.meter.record(folded * 2)


def main():
    tracks = [Drum(), Bass()]
    start = time.perf_counter_ns()
    for track in tracks:
        track.render()
    microseconds = (time.perf_counter_ns() - start) // 1000
    drum = tracks[0].meter
    bass = tracks[1].meter
    print(f"{drum.total} {drum.peak} {len(drum.loud)} {bass.total} {bass.peak} {len(bass.loud)}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
