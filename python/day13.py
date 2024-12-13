#!/bin/python3

import re
import z3

if __name__ == '__main__':
    input = []

    with open("input.txt") as file:
        for line in file:
            input.append(line)

    a_buttons = input[0::4]
    b_buttons = input[1::4]
    prizes = input[2::4]

    # parse input
    button_regex = r'Button \w: X\+(\d+), Y\+(\d+)'
    prize_regex = r'Prize: X=(\d+), Y=(\d+)'

    a_coords = []
    b_coords = []
    prize_coords = []
    for button in a_buttons:
        for match in re.findall(button_regex, button):
            a_coords.append(list(map(int, match)))
    for button in b_buttons:
        for match in re.findall(button_regex, button):
            b_coords.append(list(map(int, match)))
    for prize in prizes:
        for match in re.findall(prize_regex, prize):
            prize_coords.append(list(map(int, match)))

    def solution(part1 = False):
        sum = 0
        for curr_a, curr_b, curr_prize in zip(a_coords, b_coords, prize_coords):
            s = z3.Optimize()

            a_presses = z3.Int('a_presses')
            b_presses = z3.Int('b_presses')

            if part1:
                s.add(a_presses * curr_a[0] + b_presses * curr_b[0] == curr_prize[0])
                s.add(a_presses * curr_a[1] + b_presses * curr_b[1] == curr_prize[1])
            else:
                s.add(a_presses * curr_a[0] + b_presses * curr_b[0] == curr_prize[0] + 10000000000000)
                s.add(a_presses * curr_a[1] + b_presses * curr_b[1] == curr_prize[1] + 10000000000000)

            # press limit
            s.add(a_presses >= 0)
            s.add(b_presses >= 0)
            if part1:
                s.add(a_presses <= 100)
                s.add(b_presses <= 100)

            # get cost
            cost = z3.Int('cost')
            s.add(cost == a_presses * 3 + b_presses)
            s.minimize(cost)

            if s.check() == z3.sat:
                sum += s.model()[cost].as_long()

        return sum

    print(f"Solution 1: {solution(True)}")
    print(f"Solution 2: {solution()}")
