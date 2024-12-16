#!/bin/python3

import sys
from queue import PriorityQueue

DX = [0,  0, 1, -1]
DY = [1, -1, 0,  0]

def part1(map, start_x, start_y, end_x, end_y):
    # dijkstra
    p = PriorityQueue()
    # distance, x, y, direction
    p.put((0, start_x, start_y, 2))
    visited = set()
    distances = {}

    while not p.empty():
        curr_distance, curr_x, curr_y, curr_dir = p.get()

        if (curr_x, curr_y, curr_dir) in visited:
            continue
        visited.add((curr_x, curr_y, curr_dir))

        if (curr_x, curr_y) not in map.keys():
            continue

        for neighbour_x, neighbour_y in map[(curr_x, curr_y)]:
            delta_x = neighbour_x - curr_x
            delta_y = neighbour_y - curr_y

            # 4 possible directions
            '''
            DX = [0,  0, 1, -1]
            DY = [1, -1, 0,  0]
            '''
            new_dir = -1
            if delta_x > 0 and delta_y == 0:
                new_dir = 2
            elif delta_x < 0 and delta_y == 0:
                new_dir = 3
            elif delta_x == 0 and delta_y < 0:
                new_dir = 1
            elif delta_x == 0 and delta_y > 0:
                new_dir = 0
            else:
                raise RuntimeError

            new_distance = curr_distance + abs(delta_x) + abs(delta_y)
            if new_dir != curr_dir:
                # 180 turn
                if DX[curr_dir] == DX[new_dir] or DY[curr_dir] == DY[new_dir]:
                    new_distance += 2000
                # 90 turn
                else:
                    new_distance += 1000

            if (neighbour_x, neighbour_y) not in distances.keys() or distances[(neighbour_x, neighbour_y)] > new_distance:
                distances[(neighbour_x, neighbour_y)] = new_distance

                p.put((new_distance, neighbour_x, neighbour_y, new_dir))

    return distances[(end_x, end_y)], distances

def part2(map, start_x, start_y, end_x, end_y, optimal_distance, distances):
    visited_all = set()

    distances2 = [{}, {}, {}, {}]
    for i in range(4):
        _, distances2[i] = part1(map, end_x, end_y, start_x, start_y)
    
    visited_optimal = set()
    for key in map.keys():
        for i in range(4):
            if key not in distances2[i].keys() or key not in distances.keys():
                continue

            if distances[key] + distances2[i][key] <= optimal_distance:
                visited_optimal.add(key)

    visited_optimal.add((start_x, start_y))
    visited_optimal.add((end_x, end_y))

    for visited_x, visited_y in visited_optimal:
        for visited_x2, visited_y2 in visited_optimal:
            if (visited_x, visited_y) not in map.keys():
                continue
            elif (visited_x2, visited_y2) not in map[(visited_x, visited_y)]:
                continue

            if visited_x == visited_x2:
                min_y = min(visited_y, visited_y2)
                max_y = max(visited_y, visited_y2)

                for curr_y in range(min_y, max_y+1):
                    visited_all.add((visited_x, curr_y))
            elif visited_y == visited_y2:
                min_x = min(visited_x, visited_x2)
                max_x = max(visited_x, visited_x2)

                for curr_x in range(min_x, max_x+1):
                    visited_all.add((curr_x, visited_y))
            else:
                raise RuntimeError


    return len(visited_all)

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    input = []
    with open("input.txt") as file:
        for line in file:
            input.append(line.strip())

    # preprocess map to add just intersections
    new_map = {}
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == 'S':
                start_x = j
                start_y = i
            elif input[i][j] == 'E':
                end_x = j
                end_y = i

    visited = set()
    def recursion(start_x, start_y, x, y, direction):
        next_x = x + DX[direction]
        next_y = y + DY[direction]

        if (start_x, start_y, x, y, direction) in visited:
            return
        visited.add((start_x, start_y, x, y, direction))

        # check if you're at an intersection'
        if DX[direction] == 0 and input[next_y][next_x] != '#' and (input[next_y][next_x + 1] != '#' or input[next_y][next_x - 1] != '#'):
            if (start_x, start_y) not in new_map.keys():
                new_map[(start_x, start_y)] = set()
            new_map[(start_x, start_y)].add((next_x, next_y))

            if input[next_y][next_x - 1] != '#':
                recursion(next_x, next_y, next_x, next_y, 3)
            if input[next_y][next_x + 1] != '#':
                recursion(next_x, next_y, next_x, next_y, 2)
        elif DY[direction] == 0 and input[next_y][next_x] != '#' and (input[next_y + 1][next_x] != '#' or input[next_y - 1][next_x] != '#'):
            if (start_x, start_y) not in new_map.keys():
                new_map[(start_x, start_y)] = set()
            new_map[(start_x, start_y)].add((next_x, next_y))

            if input[next_y - 1][next_x] != '#':
                recursion(next_x, next_y, next_x, next_y, 1)
            if input[next_y + 1][next_x] != '#':
                recursion(next_x, next_y, next_x, next_y, 0)

        # just continue if you can
        if input[next_y][next_x] != '#':
            recursion(start_x, start_y, next_x, next_y, direction)
            return

        # no movement
        if start_x == x and start_y == y:
            return

        # there was some movement, add the intersection to the new map
        if (start_x, start_y) not in new_map.keys():
            new_map[(start_x, start_y)] = set()
        new_map[(start_x, start_y)].add((x, y))

        # check possible new directions
        for new_dir in range(4):
            recursion(x, y, x, y, new_dir)

    # generate new map
    for dir in range(4):
        recursion(start_x, start_y, start_x, start_y, dir)

    optimal_distance, distances = part1(new_map, start_x, start_y, end_x, end_y)
    print(f"Solution 1: {optimal_distance}")
    print(f"Solution 2: {part2(new_map, start_x, start_y, end_x, end_y, optimal_distance, distances)}")
