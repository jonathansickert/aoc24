from aoc24.aoc_decorator import solves_puzzle


def combo(operand: int, registers: list[int]) -> int:
    if operand in {0, 1, 2, 3}:
        return operand
    if operand in {4, 5, 6}:
        return registers[operand - 4]
    raise ValueError


def adv(operand: int, registers: list[int]) -> int:
    return registers[0] // (2 ** combo(operand, registers))


def bxl(operand: int, registers: list[int]) -> int:
    return operand ^ registers[1]


def bst(operand: int, registers: list[int]) -> int:
    return combo(operand, registers) % 8


def jnz(operand: int, registers: list[int]) -> int:
    if registers[0] == 0:
        return -1
    return operand


def bxc(operand: int, registers: list[int]) -> int:
    return registers[1] ^ registers[2]


def out(operand: int, registers: list[int]) -> int:
    return combo(operand, registers) % 8


def bdv(operand: int, registers: list[int]) -> int:
    return registers[0] // 2 ** combo(operand, registers)


def cdv(operand: int, registers: list[int]) -> int:
    return registers[0] // 2 ** combo(operand, registers)


function_lookup = {
    0: (adv, 0),
    1: (bxl, 1),
    2: (bst, 1),
    3: (jnz, 1000),
    4: (bxc, 1),
    5: (out, 1000),
    6: (bdv, 1),
    7: (cdv, 2),
}


def run_program(registers: list[int], program: list[int]) -> list[int]:
    counter: int = 0
    output: list[int] = []
    ops: list[int] = []
    while counter + 1 < len(program):
        opcode: int = program[counter]
        operand: int = program[counter + 1]
        operation, target_register = function_lookup[opcode]
        result: int = operation(operand, registers)
        ops.append(opcode)
        if operation == out:
            output.append(result)
        elif operation == jnz:
            if result != -1:
                counter = result
                continue
        else:
            registers[target_register] = result
        counter += 2
    return output


@solves_puzzle(day=17, part=1)
def solve_part_1(input: str) -> int:
    lines: list[str] = input.splitlines()
    registers: list[int] = []
    for i in range(3):
        register = int(lines[i][12:])
        registers.append(register)
    program = list(map(int, lines[-1][9:].split(",")))
    output: list[int] = run_program(registers, program)
    print(",".join(list(map(str, output))))
    return 0


if __name__ == "__main__":
    solve_part_1()