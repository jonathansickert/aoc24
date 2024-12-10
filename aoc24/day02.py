from aoc24.aoc_decorator import solves_puzzle, to_int_grid


def is_safe(record: list[int]) -> bool:
    diff: list[int] = [record[i + 1] - record[i] for i in range(len(record) - 1)]
    if diff[0] > 0:  # ascending
        return all(1 <= x <= 3 for x in diff)
    return all(-3 <= x <= -1 for x in diff)  # descending


@solves_puzzle(day=2)
def solve_both_parts(input: str) -> tuple[int, int]:
    grid: list[list[int]] = to_int_grid(input)
    answer1: int = 0
    answer2: int = 0
    for record in grid:
        if is_safe(record):
            answer1 += 1
            answer2 += 1
        else:
            for i in range(0, len(record)):
                if is_safe(record[:i] + record[i + 1 :]):
                    answer2 += 1
                    break
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
