from datetime import datetime
from functools import wraps
from typing import Any, Callable, Protocol, Sequence

from aoc24.input import read_puzzle_input


class SolveAocPuzzle(Protocol):
    def __call__(self, /, input: str) -> int | tuple[int, int]: ...


def solves_puzzle(
    day: int, part: int | None = None
) -> Callable[[SolveAocPuzzle], Callable[[], int | tuple[int, int]]]:
    def decorator(function: SolveAocPuzzle) -> Callable[[], int | tuple[int, int]]:
        @wraps(function)
        def wrapper() -> int | tuple[int, int]:
            input: str = read_puzzle_input(day=day)
            start: datetime = datetime.now()
            answer: int | tuple[int, int] = function(input)
            match answer, part:
                case int(), int():
                    print(answer)
                    print(
                        f"{(datetime.now() - start).total_seconds():.6f}s (Part {part})"
                    )
                case (int(), int()), None:
                    print(answer[0])
                    print(answer[1])
                    print(
                        f"{(datetime.now() - start).total_seconds():.6f}s (Part 1 + Part 2)"
                    )
                case _:
                    raise NotImplementedError
            return answer

        return wrapper

    return decorator


def to_str_grid(input: str, /) -> list[str]:
    return [line for line in input.split("\n") if line]


def to_int_grid(input: str, /) -> list[list[int]]:
    return [list(map(int, line.split())) for line in to_str_grid(input)]


def to_int_grid2(input: str, /) -> list[list[int]]:
    return [list(map(int, line)) for line in to_str_grid(input)]


def isinbound(x: int, y: int, grid: Sequence[Sequence[Any]]) -> bool:
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])
