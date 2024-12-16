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


# def move_horizontal()


# def is_blocked_vertical(
#     left_x: int,
#     left_y: int,
#     right_x: int,
#     right_y: int,
#     dx: int,
#     grid: list[list[str]],
# ) -> bool:
#     if grid[left_x + dx][left_y] == "." and grid[right_x + dx][right_y] == ".":
#         return False

#     if grid[left_x + dx][left_y] == "[":
#         return is_blocked_vertical(left_x + dx, left_y, right_x + dx, right_y, dx, grid)

#     left: bool = False
#     right: bool = False
#     if grid[left_x + dx][left_y] == "]":
#         left = is_blocked_vertical(
#             left_x + dx, left_y - 1, left_x + dx, left_y, dx, grid
#         )

#     if grid[right_x + dx][right_y] == "[":
#         right = is_blocked_vertical(
#             right_x + dx, right_y, right_x + dx, right_y + 1, dx, grid
#         )

#     return left or right


# def simulate_step_3(cur_x, cur_y, move, boxes: set[Box], obstacles: set):
#     visited = set()

#     def is_blocked_vertical(x: int, y: int, dx: int) -> bool:
#         if (x, y) in boxes:
#             visited.add()

# def get_boxes_in_direction(cur_x, cur_y, dx, dy, grid: list[str]):


def simulate_step_2(
    curx: int, cury: int, move: str, boxes: set, obstacles: set, grid: list[str]
) -> tuple[int, int]:

    visited = set()

    def is_blocked_vertical(left_x: int, left_y: int, dx: int) -> bool:
        if (left_x, left_y) in boxes:
            visited.add((left_x, left_y))

        if (
            left_x + dx,
            left_y,
        ) in obstacles or (left_x + dx, left_y + 1) in obstacles:
            # print("obstacle")
            return True

        if (
            (left_x + dx, left_y - 1) not in boxes
            and (left_x + dx, left_y) not in boxes
            and (left_x + dx, left_y + 1) not in boxes
        ):
            return False

        left: bool = False
        right: bool = False
        if (left_x + dx, left_y) in boxes:
            return is_blocked_vertical(left_x + dx, left_y, dx)

        if (left_x + dx, left_y - 1) in boxes:
            left = is_blocked_vertical(left_x + dx, left_y - 1, dx)

        if (left_x + dx, left_y + 1) in boxes:
            right = is_blocked_vertical(left_x + dx, left_y + 1, dx)

        return left or right

    def is_blocked_horizontal_left(left_x: int, left_y: int) -> bool:
        if (left_x, left_y) in boxes:
            visited.add((left_x, left_y))
        if (left_x, left_y - 1) in obstacles:
            return True
        if (left_x, left_y - 2) not in boxes:
            return False
        return is_blocked_horizontal_left(left_x, left_y - 2)

    def is_blocked_horizontal_right(left_x: int, left_y: int) -> bool:
        if (left_x, left_y) in boxes:
            visited.add((left_x, left_y))
        if (left_x, left_y + 2) in obstacles:
            return True
        if (left_x, left_y + 2) not in boxes:
            return False
        return is_blocked_horizontal_right(left_x, left_y + 2)

    dx, dy = step_lookup[move]
    blocked: bool = False
    if dx in {-1, 1}:
        # print(grid[curx + dx][cury])
        if (curx + dx, cury) in obstacles:
            blocked = True
        elif (curx + dx, cury) in boxes:  # [
            blocked = is_blocked_vertical(curx + dx, cury, dx)
        elif (curx + dx, cury - 1) in boxes:  # ]
            blocked = is_blocked_vertical(curx + dx, cury - 1, dx)
    if dy == -1:
        # if (curx, cury) in
        blocked = is_blocked_horizontal_left(curx, cury)
    if dy == 1:
        if (curx, cury + 1) in obstacles:
            blocked = True
        elif (curx, cury + 1) in boxes:
            # print("in box")
            blocked = is_blocked_horizontal_right(curx, cury + 1)

    # print(blocked)
    # print(blocked)
    # print(visited)

    if blocked:
        return curx, cury

    for x, y in visited:
        boxes.remove((x, y))
        # boxes.add((x + dx, y + dy))
    for x, y in visited:
        boxes.add((x + dx, y + dy))

    return curx + dx, cury + dy


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


@solves_puzzle(day=15, part=1)
def solve_part_1(input: str) -> int:
    _grid, _moves = input.split("\n\n")
    grid: list[list[str]] = [list(line) for line in _grid.split("\n")]
    moves: str = _moves.replace("\n", "")
    answer1: int = 0
    x, y = find_initial_pos(grid)
    for move in moves:
        x, y = simulate_step(x, y, move, grid)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "O":
                answer1 += 100 * x + y
    return answer1


def print_grid(cur_x, cur_y, boxes, obstacles, grid):
    skip = False
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if skip:
                skip = False
                continue
            if x == cur_x and y == cur_y:
                print("@", end="")
            elif (x, y) in boxes:
                print("[]", end="")
                skip = True
            elif (x, y) in obstacles:
                print("#", end="")
            else:
                print(".", end="")
        print()


@solves_puzzle(day=15, part=2)
def solve_part_2(input: str) -> int:
    _grid, _moves = input.split("\n\n")
    moves: str = _moves.replace("\n", "")
    grid: list[str] = [
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        for line in _grid.splitlines()
    ]
    # grid = _grid.splitlines()
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
    # print(len(boxes))
    # for line in grid:
    #     print(line)
    # print_grid(cur_x, cur_y, boxes, obstacles, grid)
    # print()
    for move in moves:
        cur_x, cur_y = simulate_step_2(cur_x, cur_y, move, boxes, obstacles, grid)
        # print(move)
        # print_grid(cur_x, cur_y, boxes, obstacles, grid)
        # print(cur_x, cur_y)
    # print_grid(cur_x, cur_y, boxes, obstacles, grid)
    # print(cur_x, cur_y)
    # print(len(boxes))
    return sum(x * 100 + y for x, y in boxes)


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
