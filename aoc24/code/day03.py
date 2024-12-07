import re

from aoc24.input import read_input

input: str = read_input(day=3)
answer_1: int = 0
answer_2: int = 0

pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
operands_pattern = r"mul\((\d+),(\d+)\)"
operations = re.findall(pattern=pattern, string=input)
do = True

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
    answer_1 += a * b
    answer_2 += a * b if do is True else 0


print(answer_1)
print(answer_2)
