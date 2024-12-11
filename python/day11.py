#!/bin/python3

from copy import copy
from functools import cache

def perform_step(state):
    new_state = []

    for num in state:
        if int(num) == 0:
            new_state.append('1')
        elif len(num) % 2 == 0:
            new_state.append(str(int(num[:len(num)//2])))
            new_state.append(str(int(num[len(num)//2:])))
        else:
            new_state.append(str(int(num) * 2024))

    return new_state

@cache
def get_numbers(curr_number, steps_remaining):
    '''
    return how many numbers curr_number makes after steps_remaining steps
    '''
    if steps_remaining == 0:
        return 1

    if int(curr_number) == 0:
        return get_numbers('1', steps_remaining - 1)
    elif len(curr_number) % 2 == 0:
        return get_numbers(str(int(curr_number[:len(curr_number)//2])), steps_remaining - 1)\
             + get_numbers(str(int(curr_number[len(curr_number)//2:])), steps_remaining - 1)
    else:
        return get_numbers(str(int(curr_number) * 2024), steps_remaining - 1)

if __name__ == '__main__':
    input = ""
    with open("input.txt") as file:
        input = file.readline().strip()

    # PART 1
    input = input.split(' ')
    state = copy(input)
    for _ in range(25):
        state = perform_step(state)

    print(f"Solution 1: {len(state)}")

    # PART 2
    ctr = 0
    for num in input:
        ctr += get_numbers(num, 75)
    print(f"Solution 2: {ctr}")
