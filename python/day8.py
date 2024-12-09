#!/bin/python3

def part1(antennas, max_x, max_y):
    locations = set()
    for lista in antennas.values():
        for i in range(len(lista)):
            for j in range(i+1, len(lista)):
                dx = lista[j][0] - lista[i][0]
                dy = lista[j][1] - lista[i][1]

                # else they might have a node
                node1 = (lista[i][0] - dx  , lista[i][1]   - dy)
                node2 = (lista[i][0] + 2*dx, lista[i][1] + 2*dy)

                if node1[0] >= 0 and node1[0] < max_x and node1[1] >= 0 and node1[1] < max_y:
                    locations.add(node1)
                if node2[0] >= 0 and node2[0] < max_x and node2[1] >= 0 and node2[1] < max_y:
                    locations.add(node2)
    return len(locations)

def part2(antennas, max_x, max_y):
    locations = set()
    for lista in antennas.values():
        for i in range(len(lista)):
            for j in range(i+1, len(lista)):
                dx = lista[j][0] - lista[i][0]
                dy = lista[j][1] - lista[i][1]

                # else they might have a node
                locations.add(lista[i])
                node1 = (lista[i][0] - dx, lista[i][1] - dy)
                node2 = (lista[i][0] + dx, lista[i][1] + dy)

                while node1[0] >= 0 and node1[0] < max_x and node1[1] >= 0 and node1[1] < max_y:
                    locations.add(node1)
                    node1 = (node1[0] - dx, node1[1] - dy)

                while node2[0] >= 0 and node2[0] < max_x and node2[1] >= 0 and node2[1] < max_y:
                    locations.add(node2)
                    node2 = (node2[0] + dx, node2[1] + dy)

    return len(locations)

if __name__ == '__main__':
    map = []

    with open("input.txt") as file:
        for line in file:
            map.append(line.strip())

    antennas = {}
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == '.':
                continue
            
            if cell in antennas.keys():
                antennas[cell].append((x, y))
            else:
                antennas[cell] = [(x, y)]

    print(f"Solution 1: {part1(antennas, len(map), len(map[0]))}")
    print(f"Solution 2: {part2(antennas, len(map), len(map[0]))}")
