from aoc24.aoc_decorator import solves_puzzle


@solves_puzzle(day=1)
def solve_both_parts(input: str) -> tuple[int, int]:
    vals: list[str] = input.split()
    left: list[int] = sorted(int(val) for i, val in enumerate(vals) if i % 2 == 0)
    right: list[int] = sorted(int(val) for i, val in enumerate(vals) if i % 2 == 1)
    answer1: int = sum([abs(left[i] - right[i]) for i in range(len(left))])
    answer2: int = sum([left[i] * right.count(left[i]) for i in range(len(left))])
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
