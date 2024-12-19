#!/bin/python3

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

if __name__ == '__main__':
    availible = []
    desired = []

    with open("input.txt") as file:
        content = file.readlines()

        availible = list(map(lambda x: x.strip(), content[0].split(',')))
        desired = list(map(lambda x: x.strip(), content[2:]))


    print(f"Solution 1: {part1(availible, desired)}")
