#!/bin/python3

if __name__ == '__main__':
    input_wires = {}
    rules = []
    with open('input.txt') as file:
        inputs, rules = file.read().split('\n\n')

        for wire in inputs.split('\n'):
            wire, value = wire.split(':')
            input_wires[wire] = int(value)

        rules = list(map(lambda x: x.split(' -> '), rules.strip().split('\n')))
    
    unprocessed_wires = set(list(map(lambda x: x[1], rules)))
    while unprocessed_wires != set():
        for rule in rules:
            if rule[1] not in unprocessed_wires:
                continue

            operand1, operator, operand2 = rule[0].split(' ')
            if operand1 not in input_wires or operand2 not in input_wires:
                continue

            res = 0
            if operator == 'AND':
                res = input_wires[operand1] & input_wires[operand2]
            elif operator == 'OR':
                res = input_wires[operand1] | input_wires[operand2]
            elif operator == 'XOR':
                res = input_wires[operand1] ^ input_wires[operand2]
            else:
                raise RuntimeError

            input_wires[rule[1]] = res
            unprocessed_wires.remove(rule[1])

    result = 0
    ctr = 0
    for wire in sorted(filter(lambda x: x[0] == 'z', map(lambda x: x[1], rules[::-1]))):
        result += input_wires[wire] * 2**ctr
        ctr += 1
    print(result)
