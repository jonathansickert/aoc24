import re

from aoc24.aoc_decorator import solves_puzzle


def compute_min_solution_using_cramers_rule(
    xa: int, ya: int, xb: int, yb: int, xt: int, yt: int
) -> tuple[float, float] | None:
    """Solves Ax=b according to Carmer's rule"""

    det_A = xa * yb - xb * ya
    if det_A == 0:
        return None
    det_A1 = xt * yb - xb * yt
    det_A2 = xa * yt - xt * ya
    return det_A1 / det_A, det_A2 / det_A


def compute_min_cost(xa: int, ya: int, xb: int, yb: int, xt: int, yt: int) -> int:
    """Solves min c^Tx s.t Ax=b"""

    min_solution: tuple[float, float] | None = compute_min_solution_using_cramers_rule(
        xa, ya, xb, yb, xt, yt
    )
    if not min_solution:
        return 0
    na, nb = min_solution
    if na.is_integer() and nb.is_integer():
        return 3 * int(na) + int(nb)
    return 0


@solves_puzzle(day=13)
def solve_day_1(input: str) -> tuple[int, int]:
    answer1 = 0
    answer2 = 0
    for machine in input.split("\n\n"):
        vals: list[str] = re.findall(r"\d+", machine)
        assert len(vals) == 6
        xa, ya, xb, yb, xt, yt = tuple(map(int, vals))
        answer1 += compute_min_cost(xa, ya, xb, yb, xt, yt)
        answer2 += compute_min_cost(
            xa, ya, xb, yb, xt + 10000000000000, yt + 10000000000000
        )
    return answer1, answer2


if __name__ == "__main__":
    solve_day_1()
