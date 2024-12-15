#!/bin/python3

from copy import deepcopy

DX = { '<' : -1, '>' : 1, '^' :  0, 'v' : 0 }
DY = { '<' :  0, '>' : 0, '^' : -1, 'v' : 1 }

def move_robot(map, x, y, dx, dy):
    if map[y + dy][x + dx] == '#':
        return x, y

    start_x = x
    start_y = y
    while True:
        x = x + dx
        y = y + dy
        if map[y][x] == '#':
            return start_x, start_y
        elif map[y][x] == '.':
            # we found the position where to move
            break

    curr_x = x
    curr_y = y
    while True:
        prev_x = curr_x - dx
        prev_y = curr_y - dy

        map[curr_y][curr_x] = map[prev_y][prev_x]

        curr_x = prev_x
        curr_y = prev_y

        if curr_x == start_x and curr_y == start_y:
            map[curr_y][curr_x] = '.'
            break

    return start_x + dx, start_y + dy

def simulate_robot(map, instructions):
    x = 1
    y = 1
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '@':
                x = j
                y = i
                break

    for instruction in instructions:
        x, y = move_robot(map, x, y, DX[instruction], DY[instruction])

        '''
        print(f"Move {instruction}:")
        print()
        for line in map:
            print(''.join(line))
        '''

    cost = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'O':
                cost += 100 * i + j

    return cost

def move_robot2(map, x, y, dx, dy):
    # for left / right it is the same as usual
    if dy == 0:
        return move_robot(map, x, y, dx, dy)
    assert dx == 0

    # Three cases, there is a wall, there is empty space, there is a box

    # the boxes are sharing the same y coords, but have different x coords
    left_x = x
    right_x = x

    if map[y + dy][x] == '#':
        return x, y
    elif map[y + dy][x] == '.':
        map[y][x] = '.'
        map[y + dy][x] = '@'
        return x + dx, y + dy
    elif map[y + dy][x] == '[':
        left_x = x
        right_x = x + 1
    elif map[y + dy][x] == ']':
        left_x = x - 1
        right_x = x
    else:
        raise RuntimeError

    def move_box(map, y, left_x, right_x) -> bool:
        next_y = y + dy

        # we ran into a box and try to move it
        # Four possibilities:
        # [].  []  .[]  [][]
        #  []  []  []    []
        allowed_to_move = True
        if map[next_y][left_x] == '[' and map[next_y][right_x] == ']':
            allowed_to_move = move_box(map, next_y, left_x, right_x)
        elif map[next_y][left_x] == ']' and map[next_y][right_x] == '[':
            backup_map = deepcopy(map)
            allowed_to_move = move_box(map, next_y, left_x-1, left_x) and\
                              move_box(map, next_y, right_x, right_x+1)
            if not allowed_to_move:
                for i in range(len(map)):
                    for j in range(len(map[0])):
                        map[i][j] = backup_map[i][j]

        elif map[next_y][left_x] == ']' and map[next_y][right_x] == '.':
            allowed_to_move = move_box(map, next_y, left_x-1, left_x)
        elif map[next_y][right_x] == '[' and map[next_y][left_x] == '.':
            allowed_to_move = move_box(map, next_y, right_x, right_x+1)

        if not allowed_to_move:
            return False

        # After that we should be able to move iff it is possible
        if map[next_y][left_x] == '#' or map[next_y][right_x] == '#':
            return False
        elif map[next_y][left_x] == '.' or map[next_y][right_x] == '.':
            map[y][left_x] = '.'
            map[y][right_x] = '.'

            map[next_y][left_x] = '['
            map[next_y][right_x] = ']'
            return True
        else:
            return False

    if move_box(map, y + dy, left_x, right_x):
        map[y + dy][x] = '@'
        map[y][x] = '.'
        return x, y + dy

    return x, y

def part2(map, instructions):
    new_map = []
    for line in map:
        new_line = ""
        for char in line:
            if char == '@':
                new_line += '@.'
            elif char == 'O':
                new_line += '[]'
            else:
                new_line += char * 2
        new_map.append(list(new_line))

    x = 1
    y = 1
    for i in range(len(new_map)):
        for j in range(len(new_map[0])):
            if new_map[i][j] == '@':
                x = j
                y = i
                break

    for instruction in instructions:
        x, y = move_robot2(new_map, x, y, DX[instruction], DY[instruction])

        '''
        print(f"Move {instruction}:")
        print()
        for line in new_map:
            print(''.join(line))
        '''
    cost = 0
    for i in range(len(new_map)):
        for j in range(len(new_map[0])):
            if new_map[i][j] == '[':
                cost += i * 100 + j
    return cost

if __name__ == '__main__':
    input : list[list[str]] = []
    instructions = str = ""

    with open("input.txt") as file:
        firstPart = True
        for line in file:
            if line.strip() == '':
                firstPart = False
                continue

            if firstPart:
                input.append(list(line.strip()))
            else:
                instructions += line.strip()

    print(f"Solution 1: {simulate_robot(deepcopy(input), instructions)}")
    print(f"Solution 2: {part2(input, instructions)}")
