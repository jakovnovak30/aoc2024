#!/bin/python3

from itertools import combinations
from copy import copy

if __name__ == '__main__':
    connections = {}

    with open("input.txt") as file:
        for line in file:
            first, second = line.strip().split('-')
            if first not in connections.keys():
                connections[first] = [second]
            else:
                connections[first].append(second)

            if second not in connections.keys():
                connections[second] = [first]
            else:
                connections[second].append(first)

    # PART 1
    ctr = 0
    for comp1, comp2, comp3 in combinations(connections.keys(), 3):
        if comp2 not in connections[comp1] or comp3 not in connections[comp1]:
            continue
        elif comp1 not in connections[comp2] or comp3 not in connections[comp2]:
            continue
        elif comp1 not in connections[comp3] or comp2 not in connections[comp3]:
            continue

        if comp1[0] == 't' or comp2[0] == 't' or comp3[0] == 't':
            ctr += 1
    print(f"Solution 1: {ctr}")

    # PART 2
    max_set = set()
    for comp1 in connections.keys():
        current_set = set([comp1]) # all computer that might be connected to each other
        for comp2 in connections[comp1]:
            comp2_connections = set(connections[comp2])
            if current_set.issubset(comp2_connections):
                current_set.add(comp2)

        if len(current_set) > len(max_set):
            max_set = copy(current_set)
    print(f"Solution 2: {','.join(sorted(max_set))}")
