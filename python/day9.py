#!/bin/python3

from copy import copy

def part1(disk):
    new_disk = list(copy(disk))
    j = 0
    for i, mem in enumerate(disk[::-1]):
        # get to a used chunk
        if mem == '.':
            continue
        # find free space for used chunk
        while j  < len(new_disk) and new_disk[j] != '.':
            j += 1
        if j == len(new_disk) or len(new_disk) - i - 1 <= j:
            break

        new_disk[j] = mem
        new_disk[len(new_disk) - i - 1] = '.'

    sum = 0
    for i, num in enumerate(new_disk):
        if num == '.':
            break
        sum += i * int(num)

    return sum

def part2(disk):
    new_disk = list(copy(disk))

    pass

if __name__ == '__main__':
    input = ""
    with open("input.txt") as file:
        input = file.readline().strip()

    disk = []
    ctr = 0

    if len(input[::2]) != len(input[1::2]):
        input += '0'
    for file, free in zip(input[::2], input[1::2]):
        disk += [ctr] * int(file)
        disk += ['.'] * int(free)
        ctr += 1

    print(f"Solution 1: {part1(disk)}")
    print(f"Solution 2: {part2(disk)}")
