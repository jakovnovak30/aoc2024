#!/bin/python3

def part1_recursion(result, num_list):
    if len(num_list) == 1:
        return result == num_list[0]

    return part1_recursion(result, [num_list[0]+num_list[1]] + num_list[2:])\
            or part1_recursion(result, [num_list[0]*num_list[1]] + num_list[2:])

def part2_recursion(result, num_list):
    if len(num_list) == 1:
        return result == num_list[0]

    return part2_recursion(result, [num_list[0]+num_list[1]] + num_list[2:])\
            or part2_recursion(result, [num_list[0]*num_list[1]] + num_list[2:])\
            or part2_recursion(result, [int(str(num_list[0])+str(num_list[1]))] + num_list[2:])

if __name__ == '__main__':
    results = []
    nums = []

    with open("input.txt") as file:
        for line in file:
            results.append(int(line[0:line.find(':')]))
            nums.append(list(map(int, line[line.find(':')+2:].strip().split(' '))))


    # PART 1
    sum = 0
    for result, num_list in zip(results, nums):
        if part1_recursion(result, num_list):
            sum += result
    print(f"Solution 1: {sum}")
    
    # PART 2
    sum = 0
    for result, num_list in zip(results, nums):
        if part2_recursion(result, num_list):
            sum += result
    print(f"Solution 1: {sum}")
