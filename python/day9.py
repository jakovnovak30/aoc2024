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
    potential_moves = list(filter(lambda x: x[0] != '.', disk[::-1]))

    for file in potential_moves:
        head = 0
        tail = new_disk.index(file)
        while head <= tail:
            # find free space on disk
            if new_disk[head][0] != '.':
                head += 1
                continue

            # check size
            if new_disk[head][1] < new_disk[tail][1]:
                head += 1
                continue

            # perform move
            empty_size = new_disk[head][1]
            backup_tail = new_disk[tail]
            new_disk[tail] = ('.', backup_tail[1])
            del new_disk[head]
            new_disk.insert(head, backup_tail)
            if backup_tail[1] != empty_size:
                new_disk.insert(head+1, ('.', empty_size - backup_tail[1]))

            # merge empty spaces
            new_new_disk = []
            empty_ctr = 0
            for elem in new_disk:
                if elem[0] != '.':
                    if empty_ctr != 0:
                        new_new_disk.append(('.', empty_ctr))
                    empty_ctr = 0
                    new_new_disk.append(elem)
                else:
                    empty_ctr += elem[1]
            if empty_ctr != 0:
                new_new_disk.append(('.', empty_ctr))

            new_disk = new_new_disk

            break

    array_rep = []
    for stuff, lenght in new_disk:
        array_rep += [stuff] * lenght

    sum = 0
    for i, item in enumerate(array_rep):
        if isinstance(item, int):
            sum += item * i

    return sum

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

    disk = []
    ctr = 0
    for file, free in zip(input[::2], input[1::2]):
        disk.append((ctr, int(file)))
        disk.append(('.', int(free)))
        ctr += 1

    print(f"Solution 2: {part2(disk)}")
