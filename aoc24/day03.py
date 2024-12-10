import re

from aoc24.aoc_decorator import solves_puzzle

pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
operands_pattern = r"mul\((\d+),(\d+)\)"


@solves_puzzle(day=3)
def solve_both_parts(input: str) -> tuple[int, int]:
    answer1: int = 0
    answer2: int = 0
    do = True
    operations = re.findall(pattern=pattern, string=input)
    for operation in operations:
        if operation == "do()":
            do = True
            continue
        if operation == "don't()":
            do = False
            continue
        operands = re.search(pattern=operands_pattern, string=operation)
        assert operands is not None
        a = int(operands.groups()[0])
        b = int(operands.groups()[1])
        answer1 += a * b
        answer2 += a * b if do is True else 0
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
