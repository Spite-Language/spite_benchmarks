"""A playlist of 16 tracks: each pass hands one track to a small method and reads its seconds again."""
import sys
import time


class Track:
    def __init__(self, seconds):
        self.seconds = seconds


class Playlist:
    def __init__(self):
        self.tracks = []

    def track_at(self, at):
        if at < 0 or at >= len(self.tracks):
            raise SystemExit(1)
        return self.tracks[at]

    def length_of(self, track):
        return track.seconds

    def listen(self, count):
        total = 0
        for index in range(count):
            at = index % 16
            total = total + self.length_of(self.track_at(at)) % 7 + self.track_at(at).seconds % 5
        return total


def main():
    playlist = Playlist()
    for index in range(16):
        playlist.tracks.append(Track(120 + index))
    start = time.perf_counter_ns()
    total = playlist.listen(10000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"total {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
