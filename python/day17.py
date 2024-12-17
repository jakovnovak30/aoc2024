#!/bin/python3

import z3

def get_combo_operand(combo_code, registers):
    if combo_code >= 0 and combo_code <= 3:
        return combo_code

    if combo_code >= 4 and combo_code <= 6:
        return registers[combo_code - 4]

    raise RuntimeError

def part1(registers, instructions) -> str:
    pc = 0

    output = []
    while pc < len(instructions):
        opcode = instructions[pc]

        match opcode:
            case 0:
                operand1 = registers[0]
                operand2 = 2**get_combo_operand(instructions[pc+1], registers)

                registers[0] = operand1 // operand2
                pc += 2
            case 1:
                operand1 = registers[1]
                operand2 = instructions[pc+1]

                registers[1] =  operand1 ^ operand2
                pc += 2
            case 2:
                combo = get_combo_operand(instructions[pc+1], registers)

                registers[1] = combo % 8
                pc += 2
            case 3:
                if registers[0] != 0:
                    pc = instructions[pc+1]
                else:
                    pc += 2
            case 4:
                registers[1] = registers[1] ^ registers[2]
                pc += 2
            case 5:
                combo = get_combo_operand(instructions[pc+1], registers)
                output.append(combo % 8)
                pc += 2
            case 6:
                operand1 = registers[0]
                operand2 = 2**get_combo_operand(instructions[pc+1], registers)

                registers[1] = operand1 // operand2
                pc += 2
            case 7:
                operand1 = registers[0]
                operand2 = 2**get_combo_operand(instructions[pc+1], registers)

                registers[2] = operand1 // operand2
                pc += 2

    return ','.join(map(str, output))

def part2(instructions) -> int:
    instructions = instructions
    opcodes = instructions[:-2:2]
    operands = instructions[1:-2:2]

    s = z3.Solver()
    iteration_count = len(instructions)
    A = [[z3.BitVec(f'A_{i}_{j}', 128) for j in range(len(opcodes)+1)] for i in range(iteration_count)]
    B = [[z3.BitVec(f'B_{i}_{j}', 128) for j in range(len(opcodes)+1)] for i in range(iteration_count)]
    C = [[z3.BitVec(f'C_{i}_{j}', 128) for j in range(len(opcodes)+1)] for i in range(iteration_count)]

    def get_combo_ref(combo_code, a, b, c, index):
        if combo_code >= 0 and combo_code <= 3:
            return z3.BitVecVal(combo_code, 128)

        if combo_code == 4:
            return a[index]
        elif combo_code == 5:
            return b[index]
        elif combo_code == 6:
            return c[index]

        raise RuntimeError

    for iteration, (a, b, c) in enumerate(zip(A, B, C)):
        if iteration == 0:
            s.add(b[0] == 0)
            s.add(c[0] == 0)
        else:
            s.add(a[0] == A[iteration-1][len(opcodes)])
            s.add(b[0] == B[iteration-1][len(opcodes)])
            s.add(c[0] == C[iteration-1][len(opcodes)])

        for index, (opcode, operand) in enumerate(zip(opcodes, operands)):
            match opcode:
                case 0:
                    operand2 = get_combo_ref(operand, a, b, c, index)

                    s.add(a[index+1] == a[index] >> operand2)
                    s.add(b[index+1] == b[index])
                    s.add(c[index+1] == c[index])
                case 1:
                    s.add(a[index+1] == a[index])
                    s.add(b[index+1] == b[index] ^ z3.BitVecVal(operand, 128))
                    s.add(c[index+1] == c[index])
                case 2:
                    s.add(a[index+1] == a[index])
                    s.add(b[index+1] == get_combo_ref(operand, a, b, c, index) % 8)
                    s.add(c[index+1] == c[index])
                case 4:
                    s.add(a[index+1] == a[index])
                    s.add(b[index+1] == b[index] ^ c[index])
                    s.add(c[index+1] == c[index])
                case 5:
                    s.add(a[index+1] == a[index])
                    s.add(b[index+1] == b[index])
                    s.add(c[index+1] == c[index])

                    combo = get_combo_ref(operand, a, b, c, index)
                    s.add(z3.BitVecVal(instructions[iteration], 128) == combo % 8)
                case 6:
                    operand2 = get_combo_ref(operand, a, b, c, index)

                    s.add(a[index+1] == a[index])
                    s.add(b[index+1] == a[index] >> operand2)
                    s.add(c[index+1] == c[index])
                case 7:
                    operand2 = get_combo_ref(operand, a, b, c, index)

                    s.add(a[index+1] == a[index])
                    s.add(b[index+1] == b[index])
                    s.add(c[index+1] == a[index] >> operand2)

        # conditions for a: needs to be different than zero for every iteration except the last one:
        if iteration == iteration_count - 1:
            s.add(a[len(opcodes)] == 0)
        else:
            s.add(a[len(opcodes)] != 0)

    # check model
    s.check()
    return s.model()[A[0][0]]

if __name__ == '__main__':
    registers = []
    instructions = []

    with open("input.txt") as file:
        for _ in range(3):
            registers.append(int(file.readline().strip().split(' ')[-1]))

        file.readline()
        last_line = file.readline().strip()

        instructions = list(map(int, last_line.split(' ')[-1].split(',')))

    print(f"Solution 1: {part1(registers, instructions)}")
    print(f"Solution 2: {part2(instructions)}")
