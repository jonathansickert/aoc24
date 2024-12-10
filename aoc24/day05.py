from copy import copy

from aoc24.aoc_decorator import solves_puzzle


def correct(update: list[int], rules: list[tuple[int, int]]) -> bool:
    swapped = False
    for rule in rules:
        first, second = rule
        relevant: set[int] = set(update).intersection(rule)
        update_relevant = [x for x in update if x in relevant]
        if len(update_relevant) < 2:
            continue
        if update_relevant != [first, second]:
            ifirst: int = update.index(first)
            isecond: int = update.index(second)
            update[ifirst], update[isecond] = update[isecond], update[ifirst]
            swapped |= True
    return not swapped


@solves_puzzle(day=5)
def solve_both_parts(input: str) -> tuple[int, int]:
    rules_input, updates_input = input.split("\n\n")
    rules: list[tuple[int, int]] = [
        (int(rule[0:2]), int(rule[3:5])) for rule in rules_input.split()
    ]
    updates: list[list[int]] = [
        list(map(int, update.split(sep=","))) for update in updates_input.split()
    ]
    answer1: int = 0
    answer2: int = 0
    for update in updates:
        ucopy: list[int] = copy(update)
        if correct(ucopy, rules):  # initially correct
            answer1 += ucopy[len(ucopy) // 2]
        else:
            while not correct(ucopy, rules):  # after correction
                pass
            answer2 += ucopy[len(ucopy) // 2]
    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
