from aoc24.aoc_decorator import solves_puzzle


def run_program(A_init: int, B_init: int, C_init: int, program: list[int]) -> list[int]:
    counter: int = 0
    output: list[int] = []
    A: int = A_init
    B: int = B_init
    C: int = C_init

    def combo(op: int) -> int:
        if op <= 3:
            return op
        if op == 4:
            return A
        if op == 5:
            return B
        if op == 6:
            return C
        raise AssertionError("unexpected operand: ", op)

    while counter < len(program):
        opcode: int = program[counter]
        op: int = program[counter + 1]

        if opcode == 0:
            A = A >> combo(op)
        elif opcode == 1:
            B = B ^ op
        elif opcode == 2:
            B = combo(op) % 8
        elif opcode == 3:
            if A == 0:
                pass
            else:
                counter = op
                continue
        elif opcode == 4:
            B = B ^ C
        elif opcode == 5:
            output.append(combo(op) % 8)
        elif opcode == 6:
            B = A >> combo(op)
        elif opcode == 7:
            C = A >> combo(op)

        counter += 2

    return output


def solve_with_z3(program: list[int]) -> int | None:
    from z3 import BitVec, BitVecRef, Solver, UDiv, sat

    solver = Solver()
    A: BitVecRef = BitVec("A", 64)
    # A is divided by 8 in every round (0,3).
    # The program needs to run exactly len(program) times to produce the required output.
    # Therefore, A must be high enough, that it can be divided by 8 exactly len(program) times.
    solver.add(A >= 8**15)
    solver.add(A < 8**16)

    A_cur: BitVecRef = A

    for i in range(16):
        # hardcoded chain of instructions
        out: BitVecRef = (A_cur % 8) ^ 2 ^ 3 ^ (UDiv(A_cur, 1 << ((A_cur % 8) ^ 2))) % 8
        solver.add(out == program[i])
        A_cur = UDiv(A_cur, 8)

    if solver.check() == sat:
        return solver.model()[A].as_long()  # type: ignore


def run_program_without_jmp(program: list[int], A_init: int) -> int | None:
    A: int = A_init
    B: int = 0
    C: int = 0

    opcodes: list[int] = [program[i] for i in range(len(program)) if i % 2 == 0]
    ops: list[int] = [program[i] for i in range(len(program)) if i % 2 == 1]

    assert opcodes.count(0) == 1, "expect exactly 1 adv in the program"
    assert opcodes.count(5) == 1, "expect exactly 1 out in the program"
    assert opcodes.count(3) == 1, "expect exactly 1 jnz in the program"
    assert ops[opcodes.index(0)] == 3, "expect adv instruction comes with operand 3"
    assert ops[opcodes.index(3)] == 0, "expect jnz instruction comes with operand 0"
    assert opcodes[-1] == 3, "assert last instruction is jnz"

    def combo(op: int) -> int:
        if op <= 3:
            return op
        if op == 4:
            return A
        if op == 5:
            return B
        if op == 6:
            return C
        raise AssertionError("unexpected operand: ", op)

    for opcode, op in zip(opcodes, ops):
        if opcode == 0:
            A = A >> 3
        elif opcode == 1:
            B = B ^ op
        elif opcode == 2:
            B = combo(op) % 8
        elif opcode == 4:
            B = B ^ C
        elif opcode == 5:
            return combo(op) % 8
        elif opcode == 6:
            B = A >> combo(op)
        elif opcode == 7:
            C = A >> combo(op)
        else:
            raise AssertionError("unexpected opcode: ", opcode)


def reverse_engineer(index: int, program: list[int], A_init: int) -> int | None:
    if index < 0:
        return A_init
    for d in range(8):
        A: int = (A_init << 3) + d
        out: int | None = run_program_without_jmp(program, A)
        if out == program[index]:
            next: int | None = reverse_engineer(index - 1, program, A)
            if next is not None:
                return next


@solves_puzzle(day=17, part=1)
def solve_part_1(input: str) -> int:
    lines: list[str] = input.splitlines()
    registers: list[int] = []
    for i in range(3):
        register = int(lines[i][12:])
        registers.append(register)
    program = list(map(int, lines[-1][9:].split(",")))
    output: list[int] = run_program(registers[0], registers[1], registers[2], program)
    print(",".join(list(map(str, output))))
    return 0


@solves_puzzle(day=17, part=2)
def solve_part_2(input: str) -> int:
    lines: list[str] = input.splitlines()
    program = list(map(int, lines[-1][9:].split(",")))
    answer: int | None = reverse_engineer(len(program) - 1, program, 0)
    # answer: int | None = solve_with_z3(program)
    assert answer is not None, "no solution"
    return answer


if __name__ == "__main__":
    solve_part_1()
    solve_part_2()
