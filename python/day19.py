#!/bin/python3

from functools import cache

def part1(availible : list[str], desired : list[str]) -> int:
    def check_possible(curr : str, goal : str) -> bool:
        if curr == goal:
            return True
        elif len(curr) >= len(goal) or goal[:len(curr)] != curr:
            return False

        or_part = False
        # check other options
        for next in availible:
            or_part = or_part or check_possible(curr + next, goal)

        return or_part

    ctr = 0
    for goal in desired:
        ctr += check_possible('', goal)

    return ctr

def part2(availible : list[str], desired : list[str]) -> int:
    @cache
    def check_options(curr : str, goal : str) -> int:
        if curr == goal:
            return 1
        elif len(curr) >= len(goal) or goal[:len(curr)] != curr:
            return 0

        or_part = 0
        # check other options
        for next in availible:
            or_part += check_options(curr + next, goal)

        return or_part

    ctr = 0
    for goal in desired:
        ctr += check_options('', goal)

    return ctr

if __name__ == '__main__':
    availible = []
    desired = []

    with open("input.txt") as file:
        content = file.readlines()

        availible = list(map(lambda x: x.strip(), content[0].split(',')))
        desired = list(map(lambda x: x.strip(), content[2:]))


    print(f"Solution 1: {part1(availible, desired)}")
    print(f"Solution 2: {part2(availible, desired)}")
