from collections import deque
from typing import Iterator

from aoc24.aoc_decorator import isinbound, solves_puzzle, to_int_grid2


def find_next_steps(x: int, y: int, grid) -> Iterator[tuple[int, int]]:
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for dx, dy in dirs:
        new_x, new_y = x + dx, y + dy
        if isinbound(new_x, new_y, grid) and grid[new_x][new_y] == grid[x][y] + 1:
            yield new_x, new_y


def trailhead_score_and_rating(start_x: int, start_y: int, grid) -> tuple[int, int]:
    q: deque[tuple[int, int]] = deque([(start_x, start_y)])
    ends: set[tuple[int, int]] = set()
    rating: int = 1
    while q:
        x, y = q.pop()
        if grid[x][y] == 9:  # found end
            ends.add((x, y))
            continue
        next_steps = list(find_next_steps(x, y, grid))
        rating += len(next_steps) - 1  # new paths
        q.extend(next_steps)
    return len(ends), rating


@solves_puzzle(day=10)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid: list[list[int]] = to_int_grid2(input)
    answer1: int = 0
    answer2: int = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:  # found trailhead
                score, rating = trailhead_score_and_rating(x, y, grid)
                answer1 += score
                answer2 += rating
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
