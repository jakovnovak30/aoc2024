#!/bin/python3

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

        #print(instructions[pc])
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
