"""Builds a label like "7 cacti" a million times, pluralizing the word with a lookup of uncountable and irregular words."""
import sys
import time

UNCOUNTABLES = [
    "data", "equipment", "health", "information", "rice", "money", "species", "series", "fish", "sheep", "jeans",
    "police", "deer", "moose", "aircraft", "news", "furniture", "luggage", "advice", "software", "hardware",
    "knowledge",
]

IRREGULARS = [
    ("person", "people"), ("man", "men"), ("woman", "women"), ("child", "children"), ("sex", "sexes"),
    ("move", "moves"), ("zombie", "zombies"), ("foot", "feet"), ("tooth", "teeth"), ("goose", "geese"),
    ("cactus", "cacti"), ("fungus", "fungi"), ("nucleus", "nuclei"), ("radius", "radii"),
    ("stimulus", "stimuli"), ("syllabus", "syllabi"), ("alumnus", "alumni"), ("criterion", "criteria"),
    ("phenomenon", "phenomena"), ("appendix", "appendices"), ("leaf", "leaves"), ("loaf", "loaves"),
    ("thief", "thieves"), ("hoof", "hooves"), ("hero", "heroes"), ("potato", "potatoes"), ("echo", "echoes"),
    ("veto", "vetoes"), ("torpedo", "torpedoes"),
]


def pluralize(word):
    lower = word.lower()
    for uncountable in UNCOUNTABLES:
        if lower == uncountable:
            return lower
    for singular, plural in IRREGULARS:
        if lower == singular:
            return plural
    if lower.endswith("x") or lower.endswith("ch") or lower.endswith("ss") or lower.endswith("sh"):
        return lower + "es"
    if lower.endswith("s"):
        return lower
    return lower + "s"


def label(count):
    if count == 1:
        return "1 cactus"
    return "%d %s" % (count, pluralize("cactus"))


def characters(count):
    total = 0
    for index in range(count):
        shown = label(index % 50)
        total = total + len(shown)
    return total


def main():
    start = time.perf_counter_ns()
    total = characters(1000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    print(f"characters {total}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
