#include <stdio.h>

int combo(int op, long A, long B, long C)
{
    switch (op)
    {
    case 0:
        return 0;
    case 1:
        return 1;
    case 2:
        return 2;
    case 3:
        return 3;
    case 4:
        return A;
    case 5:
        return B;
    case 6:
        return C;
    default:
        return -1;
    }
}

int xdv(int op, long A, long B, long C)
{
    return A / (1 << combo(op, A, B, C));
}

int bxl(int op, long A, long B, long C)
{
    return B ^ op;
}

int bst(int op, long A, long B, long C)
{
    return combo(op, A, B, C) % 8;
}

int jnz(int op, long A, long B, long C)
{
    if (A == 0)
    {
        return -1;
    }
    return op;
}

int bxc(int op, long A, long B, long C)
{
    return B ^ C;
}

int out(int op, long A, long B, long C)
{
    return combo(op, A, B, C) % 8;
}

int is_valid_output(int *output, int *program, int len_output, int len_program)
{
    if (len_output > len_program)
    {
        return 0;
    }
    for (int i = 0; i < len_output; i++)
    {
        if (output[i] != program[i])
        {
            return 0;
        }
    }
    return 1;
}

int run_program(long a, long b, long c, int *program, int len_program, int *output)
{
    long A = a;
    long B = b;
    long C = c;
    int counter = 0;
    int len_output = 0;
    int jmp;
    while (counter + 1 < len_program)
    {
        int opcode = program[counter];
        int op = program[counter + 1];
        switch (opcode)
        {
        case 0:
            A = xdv(op, A, B, C);
            break;
        case 1:
            B = bxl(op, A, B, C);
            break;
        case 2:
            B = bst(op, A, B, C);
            break;
        case 3:
            jmp = jnz(op, A, B, C);
            if (jmp != -1)
            {
                counter = jmp - 2;
            }
            break;
        case 4:
            B = bxc(op, A, B, C);
            break;
        case 5:
            output[len_output] = out(op, A, B, C);
            len_output++;
            break;
        case 6:
            B = xdv(op, A, B, C);
            break;
        case 7:
            C = xdv(op, A, B, C);
            break;
        default:
            break;
        }
        counter += 2;
        // if (is_valid_output(output, program, len_output, len_program) == 0)
        // {
        //     return 0;
        // }
    }
    return len_output;
    // return (len_output == len_program) & is_valid_output(output, program, len_output, len_program);
}

int main(int argc, char **argv)
{
    // int len_program = 16;
    // int program[16] = {2, 4, 1, 2, 7, 5, 1, 3, 4, 4, 5, 5, 0, 3, 3, 0};
    // int output[100];
    // int len_output = run_program(105818314457785, 0, 2, program, len_program, output);
    // for (int i = 0; i < len_output; i++)
    // {
    //     printf("%d ", len_output);
    // }
    // printf("\n");
    // for (long i = 0; i < 10000000000; i++)
    // {
    //     if (run_program(i, 0, 0, program, len_program, output) == 1)
    //     {
    //         printf("%ld\n", i);
    //         break;
    //     }
    // }
    // return 0;
    long long end = 1 << 40;
    long counter = 0;
    for (long i = 0; i < end; i++)
    {
        counter += 1;
    }
    return 0;
}
