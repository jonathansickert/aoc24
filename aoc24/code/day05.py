from copy import copy

from aoc24.input import read_input

input: str = read_input(day=5)
rules_input, updates_input = input.split("\n\n")
rules: list[tuple[int, int]] = [
    (int(rule[0:2]), int(rule[3:5])) for rule in rules_input.split()
]
updates: list[list[int]] = [
    list(map(int, update.split(sep=","))) for update in updates_input.split()
]
answer_1: int = 0
answer_2: int = 0


def correct(update: list[int]) -> bool:
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


for update in updates:
    ucopy: list[int] = copy(update)
    if correct(ucopy):  # initially correct
        answer_1 += ucopy[len(ucopy) // 2]
    else:
        while not correct(ucopy):  # after correction
            pass
        answer_2 += ucopy[len(ucopy) // 2]


print(answer_1)
print(answer_2)
