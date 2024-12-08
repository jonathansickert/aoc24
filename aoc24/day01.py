from aoc24.input import read_input_lines

lines: list[str] = read_input_lines(day=1)
left: list[int] = sorted([list(map(int, line.split()))[0] for line in lines])
right: list[int] = sorted([list(map(int, line.split()))[1] for line in lines])
answer_1: int = sum([abs(left[i] - right[i]) for i in range(len(left))])
answer_2: int = sum([left[i] * right.count(left[i]) for i in range(len(left))])

print(answer_1)
print(answer_2)
