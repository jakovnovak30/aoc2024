#!/bin/python3

import sys
from itertools import permutations
from functools import cache

@cache
def get_next_num(secret : int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216

    return secret

if __name__ == '__main__':
    input = []

    with open("input.txt") as file:
        for line in file:
            input.append(int(line.strip()))

    # PART 1
    sum = 0
    changes = []
    for num in input:
        last4 = (None, None, None, None)
        curr_changes = {}
        next = num
        
        for _ in range(2000):
            prev = next
            next = get_next_num(next)
            change = (next % 10) - (prev % 10)
            last4 = (last4[1], last4[2], last4[3], change)
            if last4 not in curr_changes:
                curr_changes[last4] = next % 10

        changes.append(curr_changes)
        sum += next


    print(f"Solution 1: {sum}")
    
    maxval = 0
    for key1 in range(-9, 9+1):
        for key2 in range(-9, 9+1):
            for key3 in range(-9, 9+1):
                for key4 in range(-9, 9+1):
                    key = (key1, key2, key3, key4)
                    sum = 0
                    for change_map in changes:
                        if key in change_map:
                            sum += change_map[key]
                    if sum > maxval:
                        maxval = max(maxval, sum)

    print(f"Solution 2: {maxval}")
