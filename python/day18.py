#!/bin/python3

from queue import Queue

def part1(input : list[tuple[int, int]]) -> int | None:
    visited = set()
    finish_time = None
    MAX_X = 70
    MAX_Y = 70

    q = Queue()
    q.put((0, 0, 0))

    while not q.empty():
        curr_x, curr_y, curr_steps = q.get()

        if (curr_x, curr_y) in visited:
            continue
        visited.add((curr_x, curr_y))

        if (curr_x, curr_y) in input:
            continue
        elif curr_x == MAX_X and curr_y == MAX_Y:
            finish_time = curr_steps
            continue
        elif curr_x > MAX_X or curr_x < 0 or curr_y > MAX_Y or curr_y < 0:
            continue

        DX = [1, -1, 0,  0]
        DY = [0,  0, 1, -1]
        for dx, dy in zip(DX, DY):
            q.put((curr_x+dx, curr_y+dy, curr_steps+1))

    return finish_time

def part2(input : list[tuple[int, int]]) -> int:
    lo = 0
    hi = len(input)

    while lo < hi:
        mid = (lo + hi) // 2
        res = part1(input[:mid])

        # upper part
        if res is None:
            hi = mid
        # lower part
        else:
            lo = mid+1
    return lo

if __name__ == '__main__':
    input = []

    with open("input.txt") as file:
        for line in file:
            x = int(line.strip().split(',')[0])
            y = int(line.strip().split(',')[1])
            input.append((x, y))


    print(f"Solution 1: {part1(input[:1024])}")
    print(f"Solution 2: {input[part2(input)-1]}")

