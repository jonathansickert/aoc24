from collections import deque
from typing import Iterator

from aoc24.input import read_input_lines

lines = read_input_lines(day=10)
grid: list[list[int]] = [list(map(int, line)) for line in lines]
answer_1: int = 0
answer_2: int = 0


def isinbound(x: int, y: int) -> bool:
    return x < len(grid) and x >= 0 and y < len(grid[0]) and y >= 0


def find_next_steps(x: int, y: int) -> Iterator[tuple[int, int]]:
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for dx, dy in dirs:
        new_x, new_y = x + dx, y + dy
        if isinbound(new_x, new_y) and grid[new_x][new_y] == grid[x][y] + 1:
            yield new_x, new_y


def trailhead_score_and_rating(start_x: int, start_y: int) -> tuple[int, int]:
    q: deque[tuple[int, int]] = deque([(start_x, start_y)])
    ends: set[tuple[int, int]] = set()
    rating: int = 1
    while q:
        x, y = q.pop()
        if grid[x][y] == 9:  # found end
            ends.add((x, y))
            continue
        next_steps = list(find_next_steps(x, y))
        rating += len(next_steps) - 1  # new paths
        q.extend(next_steps)
    return len(ends), rating


for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x][y] == 0:  # found trailhead
            score, rating = trailhead_score_and_rating(x, y)
            answer_1 += score
            answer_2 += rating

print(answer_1)
print(answer_2)
