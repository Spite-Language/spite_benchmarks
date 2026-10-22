"""An image of pixels brightened, contrasted, then measured by a histogram, a bright count and a weight sum."""
import sys
import time


class Pixel:
    def __init__(self, red, green, blue, alpha):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha


def make_pixel(seed):
    return Pixel(seed % 256, seed // 256 % 256, seed // 65536 % 256, seed // 16777216 * 2)


def divide(a, b):
    # C division truncates toward zero
    quotient = abs(a) // abs(b)
    return quotient if (a < 0) == (b < 0) else -quotient


def brightened(channel):
    lifted = channel + 16
    return lifted if lifted < 255 else 255


def contrasted(channel):
    spread = divide((channel - 128) * 5, 4) + 128
    if spread < 0:
        return 0
    return 255 if spread > 255 else spread


def brighten(pixel):
    pixel.red = brightened(pixel.red)
    pixel.green = brightened(pixel.green)
    pixel.blue = brightened(pixel.blue)


def contrast(pixel):
    pixel.red = contrasted(pixel.red)
    pixel.green = contrasted(pixel.green)
    pixel.blue = contrasted(pixel.blue)


def luminance(pixel):
    return (pixel.red * 77 + pixel.green * 150 + pixel.blue * 29) // 256


def setting_of(flag, otherwise):
    for argument in sys.argv[1:]:
        if argument.startswith(flag):
            return int(argument[len(flag):])
    return otherwise


def main():
    count = setting_of("--pixels=", 4194304)
    start = time.perf_counter_ns()
    pixels = []
    seed = 11
    for index in range(count):
        seed = seed * 48271 % 2147483647
        pixels.append(make_pixel(seed))
    made = time.perf_counter_ns()
    for pixel in pixels:
        brighten(pixel)
    for pixel in pixels:
        contrast(pixel)
    filtered = time.perf_counter_ns()
    histogram = [0] * 256
    for pixel in pixels:
        level = luminance(pixel)
        histogram[level] = histogram[level] + 1
    bright = 0
    for pixel in pixels:
        if pixel.alpha > 128 and luminance(pixel) > 100:
            bright = bright + 1
    weights = 0
    for pixel in pixels:
        weights = weights + pixel.red + pixel.green * 2 + pixel.blue * 3 + pixel.alpha * 5
    spread = 0
    for level in range(256):
        spread = spread + histogram[level] * (level % 7 + 1)
    finished = time.perf_counter_ns()
    print(f"spread {spread} bright {bright} weights {weights}")
    print(f"microseconds {(finished - start) // 1000}", file=sys.stderr)
    print(f"phases make {(made - start) // 1000} filter {(filtered - made) // 1000} measure {(finished - filtered) // 1000}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
