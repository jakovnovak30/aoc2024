use std::collections::HashSet;

use common::read_input;

// UP, RIGHT, DOWN, LEFT
static DXS : [i32; 4] = [ 0, 1, 0, -1];
static DYS : [i32; 4] = [-1, 0, 1,  0];
fn recursive_step(map : &mut Vec<Vec<char>>, curr_x : usize, curr_y : usize, direction_i : usize) {
    let rowc = map.len();
    let colc = map[0].len();

    let next_x = curr_x as i32 + DXS[direction_i];
    let next_y = curr_y as i32 + DYS[direction_i];

    if map[curr_y][curr_x] != '^' {
        map[curr_y][curr_x] = 'X'; // mark as visited
    }

    // End conditions
    if next_x < 0 || next_x as usize >= colc {
        return;
    }
    if next_y < 0 || next_y as usize >= rowc {
        return;
    }

    // Check for obstacle
    if map[next_y as usize][next_x as usize] == '#' {
        return recursive_step(map, curr_x, curr_y, (direction_i + 1) % 4);
    }

    // Default case
    recursive_step(map, next_x as usize, next_y as usize, direction_i)
}

fn part1(map : &mut Vec<Vec<char>>) -> u32 {
    let rowc = map.len();
    let colc = map[0].len();

    for r in 0..rowc {
        for c in 0..colc {
            if map[r][c] == '^' {
                recursive_step(map, c, r, 0);
            }
        }
    }

    let mut ctr = 1;
    for r in 0..rowc {
        for c in 0..colc {
            ctr += (map[r][c] == 'X') as u32;
        }
    }

    ctr
}

#[derive(Eq, PartialEq, Hash)]
struct Position {
    x : usize,
    y : usize,
    direction : usize
}

impl ToString for Position {
    fn to_string(&self) -> String {
        format!("Position  x: {}, y: {}, direction: {} ", self.x, self.y, self.direction)
    }
}

fn check_cycle(map : &Vec<Vec<char>>, curr_x : usize, curr_y : usize, direction_i : usize, visited_set : &mut HashSet<Position>) -> bool {
    let rowc = map.len();
    let colc = map[0].len();

    let next_x = curr_x as i32 + DXS[direction_i];
    let next_y = curr_y as i32 + DYS[direction_i];

    // mark as visited
    if visited_set.contains(&Position { x: curr_x, y: curr_y, direction: direction_i }) {
        return true;
    }
    visited_set.insert(Position { x: curr_x, y: curr_y, direction: direction_i });

    // End conditions
    if next_x < 0 || next_x as usize >= colc {
        return false;
    }
    if next_y < 0 || next_y as usize >= rowc {
        return false;
    }

    // Check for obstacle
    if map[next_y as usize][next_x as usize] == '#' {
        return check_cycle(map, curr_x, curr_y, (direction_i + 1) % 4, visited_set);
    }

    // Default case
    return check_cycle(map, next_x as usize, next_y as usize, direction_i, visited_set);
}

fn part2(map : &mut Vec<Vec<char>>) -> u32 {
    let rowc = map.len();
    let colc = map[0].len();

    let mut start_x = 0;
    let mut start_y = 0;

    for r in 0..rowc {
        for c in 0..colc {
            if map[r][c] == '^' {
                start_x = c; start_y = r;
                recursive_step(map, c, r, 0);
                break
            }
        }
    }

    // every 'X' except the starting position is a possible candidate for cycle
    let mut cycle_ctr = 0;
    for r in 0..rowc {
        for c in 0..colc {
            if map[r][c] == 'X' && (r != start_y || c != start_x) {
                map[r][c] = '#';

                let mut visited_set = HashSet::new();
                cycle_ctr += check_cycle(map, start_x, start_y, 0, &mut visited_set) as u32;

                map[r][c] = 'X';
            }
        }
    }

    cycle_ctr
}

fn main() {
    let input = read_input("src/input.txt");
    let mut char_vec : Vec<Vec<char>> = input.iter().map(|x| x.chars().collect()).collect();

    println!("Solution 1: {}", part1(&mut char_vec));
    println!("Solution 2: {}", part2(&mut char_vec));
}
