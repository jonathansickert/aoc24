import re

from aoc24.input import read_input_lines

lines: list[str] = read_input_lines(day=4)
answer_1: int = 0
answer_2: int = 0

# Part I
n_cols: int = len(lines[0])
n_rows: int = len(lines)
horizontals: list[str] = [""] * n_rows
verticals: list[str] = [""] * n_cols
diagonals_right: list[str] = [""] * (n_rows + n_cols - 1)
diagonals_left: list[str] = [""] * (n_rows + n_cols - 1)
xmas_pattern = r"(?=XMAS)|(?=SAMX)"

for row in range(n_rows):
    for col in range(n_cols):
        horizontals[row] += lines[row][col]
        verticals[col] += lines[row][col]
        diagonals_right[col - row] += lines[row][col]
        diagonals_left[col + row] += lines[row][col]

for line in horizontals + verticals + diagonals_left + diagonals_right:
    answer_1 += len(re.findall(pattern=xmas_pattern, string=line))

# Part II
for row in range(1, n_rows - 1):
    for col in range(1, n_cols - 1):
        if not lines[row][col] == "A":
            continue
        top_left: str = lines[row + 1][col - 1]
        top_right: str = lines[row + 1][col + 1]
        down_left: str = lines[row - 1][col - 1]
        down_right: str = lines[row - 1][col + 1]

        answer_2 += (
            1 if {top_left, down_right} == {"M", "S"} == {top_right, down_left} else 0
        )

print(answer_1)
print(answer_2)
