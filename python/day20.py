#!/bin/python3

import sys
from queue import Queue, PriorityQueue

DX = [0,  0, 1, -1]
DY = [1, -1, 0,  0]

def part1(map, start_x, start_y, end_x, end_y):
    obstacles = set()
    for r in range(1, len(map)-1):
        for c in range(1, len(map[0])-1):
            if map[r][c] == '#':
                obstacles.add((c, r))

    def bfs(ignore) -> int:
        q = Queue()
        q.put((start_x, start_y, 0))

        visited = set()
        while not q.empty():
            x, y, time = q.get()

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if x == end_x and y == end_y:
                return time

            for dx, dy in zip(DX, DY):
                new_x = x + dx
                new_y = y + dy

                if new_x < 0 or new_x >= len(map[0]):
                    continue
                if new_y < 0 or new_y >= len(map):
                    continue
                if map[new_y][new_x] == '#' and not (new_x == ignore[0] and new_y == ignore[1]):
                    continue

                # all good, go to that tile
                q.put((new_x, new_y, time+1))

        return -1

    baseline = bfs((-1, -1))
    ctr = 0
    for ignore in obstacles:
        retval = bfs(ignore)
        if retval == baseline:
            continue
        elif abs(retval - baseline) >= 100:
            ctr += 1

    return ctr

def part2(map, start_x, start_y, end_x, end_y, cheat_limit):
    def dijkstra() -> list[list[int]]:
        distances = [[sys.maxsize for _ in range(len(map[0]))] for _ in range(len(map))]
        distances[start_y][start_x] = 0
        # do dijkstra
        pq = PriorityQueue()
        # (distance, current x, current y)
        pq.put((0, start_x, start_y))
        visited = set()
        while not pq.empty():
            time, x, y = pq.get()

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if x == end_x and y == end_y:
                continue

            for dx, dy in zip(DX, DY):
                next_x = x + dx
                next_y = y + dy
                if map[next_y][next_x] != '#':
                    if distances[next_y][next_x] > distances[y][x] + 1:
                        distances[next_y][next_x] = distances[y][x] + 1
                    pq.put((time + 1, next_x, next_y))
        return distances

    distances = dijkstra()
    ctr = 0
    for r1 in range(len(map)):
        for c1 in range(len(map[0])):
            if distances[r1][c1] == sys.maxsize:
                continue

            # check point within cheat distance
            for r2 in range(len(map)):
                for c2 in range(len(map[0])):
                    if distances[r2][c2] == sys.maxsize:
                        continue

                    manhattan = abs(r2 - r1) + abs(c2 - c1)
                    if manhattan > cheat_limit:
                        continue

                    # how much it would usually cost minus how much it costs now + we have to get there
                    delta = distances[r1][c1] - distances[r2][c2] - manhattan
                    if delta >= 100:
                        ctr += 1
    return ctr

if __name__ == '__main__':
    map = []

    with open("input.txt") as file:
        for line in file:
            map.append(line.strip())

    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == 'S':
                start_x = c
                start_y = r
            elif map[r][c] == 'E':
                end_x = c
                end_y = r

    #print(f"Solution 1: {part1(map, start_x, start_y, end_x, end_y)}")
    print(f"Solution 1: {part2(map, start_x, start_y, end_x, end_y, 2)}")
    print(f"Solution 2: {part2(map, start_x, start_y, end_x, end_y, 20)}")
