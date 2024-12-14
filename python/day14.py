#!/bin/python3

import re
from functools import reduce
from operator import mul

pattern = r"p=(\d+,\d+) v=(-?\d+,-?\d+)"

def part1(positions, velocities) -> int:
    quadrant_ctrs = [0 for _ in range(4)]
    for pos, vel in zip(positions, velocities):
        end_x = (pos[0] + vel[0] * 100) % MAX_X
        end_y = (pos[1] + vel[1] * 100) % MAX_Y
        
        center_x = MAX_X // 2
        center_y = MAX_Y // 2

        if end_x == center_x or end_y == center_y:
            continue

        if end_x < center_x and end_y < center_y:
            quadrant_ctrs[0] += 1
        elif end_x > center_x and end_y < center_y:
            quadrant_ctrs[1] += 1
        elif end_x < center_x and end_y > center_y:
            quadrant_ctrs[2] += 1
        elif end_x > center_x and end_y > center_y:
            quadrant_ctrs[3] += 1
        else:
            raise RuntimeError

    return reduce(mul, quadrant_ctrs)

def part2(positions, velocities, iter_limit = 10000):
    image_dir = 'images_day14'

    for sec in range(1, iter_limit + 1):
        curr_x = 0
        curr_y = 0

        grid = [['.'] * MAX_X for _ in range(MAX_Y)]
        for pos, vel in zip(positions, velocities):
            curr_x = (pos[0] + vel[0] * sec) % MAX_X
            curr_y = (pos[1] + vel[1] * sec) % MAX_Y

            grid[curr_y][curr_x] = '#'

        with open(image_dir + f"/iter_{sec}.pbm", 'w') as file:
            file.write("P1\n101 103\n")
            for i in range(MAX_Y):
                for j in range(MAX_X):
                    if grid[i][j] == '.':
                        file.write('0')
                    else:
                        file.write('1')
                file.write('\n')


    return "Look at the file system images"

if __name__ == '__main__':
    positions : list[tuple] = []
    velocities : list[tuple] = []

    MAX_X = 101
    MAX_Y = 103
    with open("input.txt") as file:
        for line in file:
            for group in re.findall(pattern, line):
                to_int = lambda grupa: tuple(map(int, grupa.split(',')))

                positions.append(to_int(group[0]))
                velocities.append(to_int(group[1]))
    
    print(f"Solution 1: {part1(positions, velocities)}")
    print(f"Solution 2: {part2(positions, velocities)}")
