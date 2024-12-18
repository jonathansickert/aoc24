from z3 import BitVec, BitVecRef, BitVecVal, Solver, UDiv, sat
from z3.z3 import ModelRef

from aoc24.aoc_decorator import solves_puzzle


def combo(A: int, B: int, C: int, op: int) -> int:
    if op in {0, 1, 2, 3}:
        return op
    if op == 4:
        return A
    if op == 5:
        return B
    if op == 6:
        return C
    raise ValueError


def adv(A: int, B: int, C: int, op: int) -> tuple[int, int, int]:
    return UDiv(A, 1 << combo(A, B, C, op)), B, C


def bxl(A: int, B: int, C: int, op: int) -> tuple[int, int, int]:
    return A, op ^ B, C


def bst(A: int, B: int, C: int, op: int) -> tuple[int, int, int]:
    return A, combo(A, B, C, op) % 8, C


def jnz(A: int, B: int, C: int, op: int) -> int:
    if A == 0:
        return -1
    return op


def bxc(A: int, B: int, C: int, op: int) -> tuple[int, int, int]:
    return A, B ^ C, C


def out(A: int, B: int, C: int, op: int) -> int:
    return combo(A, B, C, op) % 8


def bdv(A: int, B: int, C: int, op: int) -> tuple[int, int, int]:
    return A, UDiv(A, 1 << combo(A, B, C, op)), C


def cdv(A: int, B: int, C: int, op: int) -> tuple[int, int, int]:
    return A, B, UDiv(A, 1 << combo(A, B, C, op))


function_lookup = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def run_program(registers: list[int], program: list[int]) -> list[tuple[int, int]]:
    counter: int = 0
    output: list[int] = []
    ops: list[tuple[int, int]] = []
    A, B, C = registers
    while counter + 1 < len(program):
        opcode: int = program[counter]
        operand: int = program[counter + 1]
        operation = function_lookup[opcode]
        ops.append((opcode, operand))
        if operation == out:
            output.append(out(A, B, C, operand))
        elif operation == jnz:
            jmp: int = jnz(A, B, C, operand)
            if jmp != -1:
                counter = jmp
                continue
        else:
            A, B, C = operation(A, B, C, operand)
        counter += 2
    return ops


def run_with_z3(program: list[int]) -> ModelRef | None:
    solver = Solver()
    A: BitVecRef = BitVec("A", 64)
    # A is divided by 8 in every round (0,3).
    # The program needs to run exactly len(program) times to produce the required output.
    # Therefore, A must be high enough, that it can be divided by 8 exactly len(program) times.
    solver.add(A >= 8**15)
    solver.add(A < 8**16)

    instr: list[tuple[int, int]] = [
        (program[i], program[i + 1]) for i in range(0, len(program), 2)
    ]

    A_cur: BitVecRef = A
    B_cur: BitVecRef = BitVec("B_cur", 64)
    C_cur: BitVecRef = BitVec("C_cur", 64)

    def combo(op: int) -> BitVecRef:
        if op <= 3:
            return BitVecVal(op, 64)
        if op == 4:
            return A_cur
        if op == 5:
            return B_cur
        if op == 6:
            return C_cur
        raise ValueError(op)

    for i in range(len(program)):
        # print(instr[:-1])
        for opcode, op in instr[:-1]:  # we can skip the last jnz instruction
            if opcode == 0:
                A_cur = UDiv(A_cur, combo(op))
            elif opcode == 1:
                B_cur = B_cur ^ op
            elif opcode == 2:
                B_cur = combo(op) % 8
            elif opcode == 3:
                pass
                # raise ValueError("multiple jumps?!")
            elif opcode == 4:
                B_cur = C_cur ^ B_cur
            elif opcode == 5:
                solver.add(combo(op) % 8 == program[i])
                pass
            elif opcode == 6:
                B_cur = UDiv(A_cur, combo(op))
            elif opcode == 7:
                C_cur = UDiv(A_cur, combo(op))

    if solver.check() == sat:
        return solver.model()
    else:
        print("not satisfiable")


@solves_puzzle(day=17, part=2)
def solve_part_2(input: str) -> int:
    lines: list[str] = input.splitlines()
    program = list(map(int, lines[-1][9:].split(",")))
    # ops: list[tuple[int, int]] = [op for op in chain if op[0] != 3]
    model = run_with_z3(program)
    print(model)
    return 0


if __name__ == "__main__":
    solve_part_2()
