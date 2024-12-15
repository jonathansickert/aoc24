import re

from aoc24.aoc_decorator import solves_puzzle

LEN_X: int = 101
LEN_Y: int = 103


def get_final_position(
    x: int, y: int, vx: int, vy: int, lenx: int, leny: int, seconds: int
) -> tuple[int, int]:
    return (x + seconds * vx) % lenx, (y + seconds * vy) % leny


def parse_input(input: str) -> list[list[int]]:
    return [
        list(map(int, (re.findall(r"-?\d+", line))))
        for line in input.split("\n")
        if line
    ]


@solves_puzzle(day=14, part=1)
def solve_part_1(input: str) -> int:
    q1 = q2 = q3 = q4 = 0
    seconds: int = 100
    for x, y, vx, vy in parse_input(input):
        xfinal, yfinal = get_final_position(x, y, vx, vy, LEN_X, LEN_Y, seconds)
        if xfinal < LEN_X // 2 and yfinal < LEN_Y // 2:
            q1 += 1
        if xfinal > LEN_X // 2 and yfinal < LEN_Y // 2:
            q2 += 1
        if xfinal < LEN_X // 2 and yfinal > LEN_Y // 2:
            q3 += 1
        if xfinal > LEN_X // 2 and yfinal > LEN_Y // 2:
            q4 += 1
    return q1 * q2 * q3 * q4


@solves_puzzle(day=14, part=2)
def solve_part_2(input: str) -> int:
    seconds = 6620
    grid: list[list[str]] = [["."] * LEN_X for _ in range(LEN_Y)]
    for x, y, vx, vy in parse_input(input):
        xfinal, yfinal = get_final_position(x, y, vx, vy, LEN_X, LEN_Y, seconds)
        grid[yfinal][xfinal] = "#"
    for line in grid:
        print("".join(line))
    return seconds


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
