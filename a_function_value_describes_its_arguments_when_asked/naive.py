"""Make a function value with its own description for each call, apply it and drop it."""
import sys
import time


class Scorer:
    def __init__(self, bonus):
        self.bonus = bonus

    def score(self, value):
        return value * 2 + self.bonus


class Argument:
    def __init__(self, name, class_name):
        self.name = name
        self.class_name = class_name


class FunctionValue:
    def __init__(self, name, returns, arguments, call, owner):
        self.name = name
        self.returns = returns
        self.arguments = arguments
        self.call = call
        self.owner = owner


def scorer_score_value(scorer):
    arguments = [Argument("value", "Integer")]
    return FunctionValue("score", "Integer", arguments, Scorer.score, scorer)


def apply(change, value):
    return change.call(change.owner, value)


def apply_all(scorer, count):
    applied = 0
    for index in range(count):
        change = scorer_score_value(scorer)
        scored = apply(change, index % 100)
        applied = applied + scored
    return applied


def main():
    start = time.perf_counter_ns()
    scorer = Scorer(3)
    applied = apply_all(scorer, 2000000)
    microseconds = (time.perf_counter_ns() - start) // 1000
    scoring = scorer_score_value(scorer)
    argument_count = len(scoring.arguments)
    print(f"applied {applied} arguments {argument_count}")
    print(f"microseconds {microseconds}", file=sys.stderr)


if __name__ == "__main__":
    main()
