from typing import Iterator

from aoc24.aoc_decorator import solves_puzzle

step_lookup: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def find_initial_pos(grid: list[list[str]]) -> tuple[int, int]:
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "@":
                return x, y
    raise ValueError


def simulate_step(
    curx: int, cury: int, move: str, grid: list[list[str]]
) -> tuple[int, int]:
    dx, dy = step_lookup[move]
    i: int = 1
    while 1:
        nx: int = curx + i * dx
        ny: int = cury + i * dy
        if grid[nx][ny] == "#":  # cannot move
            return curx, cury
        if grid[nx][ny] in {".", "@"}:
            break
        i = i + 1
    grid[curx + dx][cury + dy], grid[nx][ny] = grid[nx][ny], grid[curx + dx][cury + dy]
    return curx + dx, cury + dy


def simulate_step_2(
    curx: int, cury: int, move: str, boxes: set, obstacles: set
) -> tuple[int, int]:

    visited = set()
    dx, dy = step_lookup[move]
    blocked: bool = False

    def get_vertical_neighbours(left_x, left_y, dx) -> Iterator[tuple[int, int]]:
        for dy in {-1, 0, 1}:
            if (left_x + dx, left_y + dy) in boxes:
                yield left_x + dx, left_y + dy

    def is_box_blocked_vertical(left_x, left_y, dx) -> bool:
        visited.add((left_x, left_y))
        for dy in {0, 1}:
            if (left_x + dx, left_y + dy) in obstacles:
                return True
        return any(
            is_box_blocked_vertical(*neighbour, dx)
            for neighbour in get_vertical_neighbours(left_x, left_y, dx)
        )

    def get_horizontal_neighbours(left_x, left_y, dy) -> Iterator[tuple[int, int]]:
        if (left_x, left_y + 2 * dy) in boxes:
            yield left_x, left_y + 2 * dy

    def is_box_blocked_horizontal(left_x, left_y, dy) -> bool:
        visited.add((left_x, left_y))
        if dy == -1 and (left_x, left_y + dy) in obstacles:
            return True
        if dy == 1 and (left_x, left_y + 2 * dy) in obstacles:
            return True
        return any(
            is_box_blocked_horizontal(*neighbour, dy)
            for neighbour in get_horizontal_neighbours(left_x, left_y, dy)
        )

    if (curx + dx, cury + dy) in obstacles:
        return curx, cury

    if dx in {-1, 1}:
        if (box := (curx + dx, cury - 1)) in boxes:
            blocked = is_box_blocked_vertical(*box, dx)
        elif (box := (curx + dx, cury)) in boxes:
            blocked = is_box_blocked_vertical(*box, dx)
    elif dy == -1:
        if (box := (curx, cury + 2 * dy)) in boxes:
            blocked = is_box_blocked_horizontal(*box, dy)
    elif dy == 1:
        if (box := (curx, cury + dy)) in boxes:
            blocked = is_box_blocked_horizontal(*box, dy)

    if blocked:
        return curx, cury

    for x, y in visited:
        boxes.remove((x, y))
    for x, y in visited:
        boxes.add((x + dx, y + dy))

    return curx + dx, cury + dy


@solves_puzzle(day=15, part=1)
def solve_part_1(input: str) -> int:
    _grid, _moves = input.split("\n\n")
    grid: list[list[str]] = [list(line) for line in _grid.split("\n")]
    moves: str = _moves.replace("\n", "")
    x, y = find_initial_pos(grid)
    for move in moves:
        x, y = simulate_step(x, y, move, grid)
    return sum(
        100 * x + y
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == "O"
    )


@solves_puzzle(day=15, part=2)
def solve_part_2(input: str) -> int:
    _grid, _moves = input.split("\n\n")
    moves: str = _moves.replace("\n", "")
    grid: list[str] = [
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        for line in _grid.splitlines()
    ]
    boxes = set()
    obstacles = set()
    cur_x: int = 0
    cur_y: int = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "[":
                boxes.add((x, y))
            if grid[x][y] == "#":
                obstacles.add((x, y))
            if grid[x][y] == "@":
                cur_x, cur_y = x, y
    for move in moves:
        cur_x, cur_y = simulate_step_2(cur_x, cur_y, move, boxes, obstacles)
    return sum(x * 100 + y for x, y in boxes)


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
