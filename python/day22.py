#!/bin/python3

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
    for num in input:
        next = num
        for _ in range(2000):
            next = get_next_num(next)
        sum += next
    print(f"Solution 1: {sum}")
