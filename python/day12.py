#!/bin/python3

def calculate_area(symbol : str, map : list[str], r : int, c : int, visited_curr : set[tuple[int, int]]):
    '''
    recursively check if tiles are visited and add them to visited_curr in order to accumulate the area
    '''
    # knock-out conditions
    if r < 0 or r >= len(map):
        return
    elif c < 0 or c >= len(map[0]):
        return
    elif map[r][c] != symbol:
        return
    elif (r, c) in visited_curr:
        return

    visited_curr.add((r, c))
    DX = [1, -1, 0,  0]
    DY = [0,  0, 1, -1]
    for dx, dy in zip(DX, DY):
        calculate_area(symbol, map, r + dy, c + dx, visited_curr)
    

def calculate_perimeter(map : list[str], curr_plot : set[tuple[int, int]]) -> int:
    '''
    iterate through curr_plot and see how many tiles have no valid neighbours in each direction
    '''
    ctr = 0
    DX = [0,  0, 1, -1]
    DY = [1, -1, 0,  0]
    for r, c in curr_plot:
        for dx, dy in zip(DX, DY):
            # check if neighbour is not valid
            new_r = r + dy
            new_c = c + dx
            if new_r < 0 or new_r >= len(map):
                ctr += 1
            elif new_c < 0 or new_c >= len(map[0]):
                ctr += 1
            elif map[new_r][new_c] != map[r][c]:
                ctr += 1

    return ctr

def calculate_sides(map : list[str], curr_plot : set[tuple[int, int]]) -> int:
    '''
    calculate the new perimeter for part2
    '''

    # make map of outer pieces
    outer = set()
    DX = [0,  0, 1, -1]
    DY = [1, -1, 0,  0]
    for r, c in curr_plot:
        for dx, dy in zip(DX, DY):
            # check if neighbour is not valid
            new_r = r + dy
            new_c = c + dx

            symbol = ''
            if dy == 0:
                symbol = '|' if dx == 1 else '||'
            else:
                symbol = '-' if dy == 1 else '--'

            if new_r < 0 or new_r >= len(map):
                outer.add((new_r, new_c, symbol))
            elif new_c < 0 or new_c >= len(map[0]):
                outer.add((new_r, new_c, symbol))
            elif map[new_r][new_c] != map[r][c]:
                outer.add((new_r, new_c, symbol))

    # visit every side
    def visit_recursion(r, c, symbol, outer, visited):
        if (r, c, symbol) in visited:
            return
        if (r, c, symbol) not in outer:
            return
        visited.add((r, c, symbol))
        for dx, dy in zip(DX, DY):
            visit_recursion(r + dy, c + dx, symbol, outer, visited)

    visited = set()
    ctr = 0
    for r, c, symbol in outer:
        if (r, c, symbol) not in visited:
            ctr += 1
            visit_recursion(r, c, symbol, outer, visited)
        else:
            continue


    return ctr

def solution(map : list[str], part1 = True) -> int:
    R = len(map)
    C = len(map[0])

    visited = set()
    acc = 0
    for r in range(R):
        for c in range(C):
            if (r, c) not in visited:
                visited_curr = set() # used later for perimeter
                calculate_area(map[r][c], map, r, c, visited_curr)
                area_curr = len(visited_curr)
                perimeter_curr = calculate_perimeter(map, visited_curr) if part1 else calculate_sides(map, visited_curr)

                acc += area_curr * perimeter_curr
                visited = visited | visited_curr

    return acc

if __name__ == '__main__':
    map = []
    with open("input.txt") as file:
        for line in file:
            map.append(line.strip())

    print(f"Solution 1: {solution(map)}")
    print(f"Solution 2: {solution(map, False)}")
