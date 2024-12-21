from aoc24.aoc_decorator import solves_puzzle


def n_possible_arrangements(design: str, towels: list[str]) -> int:

    mem: dict[str, int] = {}

    def is_possible_rec(design: str) -> int:
        if design not in mem:
            if len(design) == 0:
                return 1
            count = 0
            for towel in towels:
                if design.startswith(towel):
                    count += is_possible_rec(design[len(towel) :])
            mem[design] = count
        return mem[design]

    return is_possible_rec(design)


@solves_puzzle(day=19)
def solve_both_parts(input: str) -> tuple[int, int]:
    towels, designs = input.split("\n\n")
    towels = towels.split(", ")
    designs = designs.splitlines()
    answer1: int = 0
    answer2: int = 0

    for design in designs:
        potential_towels: list[str] = [towel for towel in towels if towel in design]
        count: int = n_possible_arrangements(design, potential_towels)
        if count > 0:
            answer1 += 1
        answer2 += count

    return answer1, answer2


if __name__ == "__main__":
    solve_both_parts()
