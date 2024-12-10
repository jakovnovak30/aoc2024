#!/bin/python3

def check_trails(map, r, c, visited):
    if (r, c) in visited:
        return 0
    visited.add((r, c))
    if map[r][c] == '9':
        return 1

    # check all directions
    DX = [1, -1, 0,  0]
    DY = [0,  0, 1, -1]
    ret = 0
    for dx, dy in zip(DX, DY):
        new_r = r + dy
        new_c = c + dx

        if new_r < 0 or new_r >= len(map):
            continue
        if new_c < 0 or new_c >= len(map[0]):
            continue

        if int(map[new_r][new_c]) == int(map[r][c]) + 1:
            ret += check_trails(map, new_r, new_c, visited)

    return ret

def check_rating(map, r, c):
    if map[r][c] == '9':
        return 1

    # check all directions
    DX = [1, -1, 0,  0]
    DY = [0,  0, 1, -1]
    ret = 0
    for dx, dy in zip(DX, DY):
        new_r = r + dy
        new_c = c + dx

        if new_r < 0 or new_r >= len(map):
            continue
        if new_c < 0 or new_c >= len(map[0]):
            continue

        if int(map[new_r][new_c]) == int(map[r][c]) + 1:
            ret += check_rating(map, new_r, new_c)

    return ret

def part1(map):
    ctr = 0
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == '0':
                ctr += check_trails(map, r, c, set())
    return ctr

def part2(map):
    ctr = 0
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == '0':
                ctr += check_rating(map, r, c)
    return ctr

if __name__ == '__main__':
    input = []
    with open("input.txt") as file:
        for line in file:
            input.append(line.strip())


    print(f"Solution 1: {part1(input)}")
    print(f"Solution 2: {part2(input)}")
