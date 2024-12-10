import re

from aoc24.aoc_decorator import solves_puzzle, to_str_grid


@solves_puzzle(day=4, part=1)
def solve_part_1(input: str) -> int:
    grid: list[str] = to_str_grid(input)
    answer1: int = 0
    n_cols, n_rows = len(grid[0]), len(grid)
    horizontals: list[str] = [""] * n_rows
    verticals: list[str] = [""] * n_cols
    diagonals_right: list[str] = [""] * (n_rows + n_cols - 1)
    diagonals_left: list[str] = [""] * (n_rows + n_cols - 1)
    xmas_pattern = r"(?=XMAS)|(?=SAMX)"
    for x in range(n_rows):
        for y in range(n_cols):
            horizontals[x] += grid[x][y]
            verticals[y] += grid[x][y]
            diagonals_right[y - x] += grid[x][y]
            diagonals_left[y + x] += grid[x][y]
    for line in horizontals + verticals + diagonals_left + diagonals_right:
        answer1 += len(re.findall(pattern=xmas_pattern, string=line))
    return answer1


@solves_puzzle(day=4, part=2)
def solve_part_2(input: str) -> int:
    grid: list[str] = to_str_grid(input)
    answer2: int = 0
    n_cols, n_rows = len(grid[0]), len(grid)
    for row in range(1, n_rows - 1):
        for col in range(1, n_cols - 1):
            if not grid[row][col] == "A":
                continue
            top_left: str = grid[row + 1][col - 1]
            top_right: str = grid[row + 1][col + 1]
            down_left: str = grid[row - 1][col - 1]
            down_right: str = grid[row - 1][col + 1]
            if {top_left, down_right} == {"M", "S"} == {top_right, down_left}:
                answer2 += 1
    return answer2


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
