#!/bin/python3

from functools import cache
from itertools import pairwise, permutations

@cache
def get_deltas(curr, next):
    if curr == next:
        return 0, 0

    if len(set(curr+next).intersection("<>v^")) > 0:
        keypad = "X^A<v>"
    else:
        keypad = "789456123X0A"

    x1, y1 = keypad.index(curr) % 3, keypad.index(curr) // 3
    x2, y2 = keypad.index(next) % 3, keypad.index(next) // 3

    return x2-x1, y2-y1

@cache
def is_valid(curr, next, pattern):
    if len(set(curr+next).intersection("<>v^")) > 0:
        keypad = "X^A<v>"
    else:
        keypad = "789456123X0A"

    x1, y1 = keypad.index(curr) % 3, keypad.index(curr) // 3

    delta = {'<' : (-1, 0), '>' : (1, 0), 'v' : (0, 1), '^' : (0, -1)}
    curr_x, curr_y = (x1, y1)
    for delta_char in pattern:
        curr_delta = delta[delta_char]
        curr_x += curr_delta[0]
        curr_y += curr_delta[1]

        if curr_x < 0 or curr_x >= 3:
            return False
        if curr_y < 0 or curr_y >= len(keypad) // 3:
            return False

        if keypad[curr_x + curr_y*3] == 'X':
            return False

    return True

@cache
def get_all_paths(curr, next):
    paths = []
    delta_x, delta_y = get_deltas(curr, next)
    cx = '>' if delta_x > 0 else '<'
    cy = '^' if delta_y < 0 else 'v'

    original_pattern = cx * abs(delta_x) + cy * abs(delta_y)
    for pattern in permutations(original_pattern):
        if is_valid(curr, next, pattern):
            paths.append(''.join(pattern) + 'A')

    return paths

@cache
def get_min_cost(target, depth):
    target = 'A' + target
    retval = 0
    for curr, next in pairwise(target):
        paths = get_all_paths(curr, next)

        if depth == 0:
            retval += min(len(path) for path in paths)
        else:
            retval += min(get_min_cost(path, depth-1) for path in paths)
    return retval

def part1(input : list[str]):
    sum = 0
    for line in input:
        sum += get_min_cost(line, 2) * int(line[:-1])
    return sum

def part2(input : list[str]):
    sum = 0
    for line in input:
        sum += get_min_cost(line, 25) * int(line[:-1])
    return sum

if __name__ == '__main__':
    input = []

    with open("input.txt") as file:
        for line in file:
            input.append(line.strip())

    print(f"Solution 1: {part1(input)}")
    print(f"Solution 2: {part2(input)}")
