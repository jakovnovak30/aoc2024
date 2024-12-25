#!/bin/python3

if __name__ == '__main__':
    maps = []
    with open('input.txt') as file:
        input = file.read()
        maps = list(map(lambda x: list(filter(lambda y: y != '', x)), map(lambda x: x.split('\n'), input.split('\n\n'))))

    locks = []
    keys = []
    colsize = len(maps[0][0])
    for map in maps:
        hash_ctr = [-1] * colsize
        for col in range(colsize):
            for row in range(len(map)):
                hash_ctr[col] += map[row][col] == '#'

        if map[0][0] == '#':
            # lock
            locks.append(hash_ctr)
        else:
            # key
            keys.append(hash_ctr)

    rowcount = len(maps[0])
    solution = 0
    for lock in locks:
        for key in keys:
            valid = True
            for col in range(colsize):
                if lock[col] + key[col] >= rowcount-1:
                    valid = False
                    break
            #print(f"Lock: {lock}, key: {key}, overlap: {not valid}")
            solution += valid
    print(f"Solution: {solution}")
