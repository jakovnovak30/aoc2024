use common::read_input;

// LEFT, RIGHT, DOWN, UP, DIAG_NW, DIAG_NE, DIAG_SW, DIAG_SE
static DXS : [i32; 8] = [-1, 1,  0, 0, -1, 1, -1,  1];
static DYS : [i32; 8] = [ 0, 0, -1, 1,  1, 1, -1, -1];
fn check_recursively(x : u32, y : u32, dx : i32, dy : i32, last_char : char, input : &Vec<Vec<char>>) -> bool {
    let next_x = x as i32 + dx;
    let next_y = y as i32 + dy;

    // bounds check
    if next_x < 0 || next_x >= input[0].len() as i32 {
        return false;
    }
    if next_y < 0 || next_y >= input.len() as i32 {
        return false;
    }

    // get next char and check if it's the right one
    let next_char = input[next_y as usize][next_x as usize];

    if last_char == 'X' && next_char == 'M' {
        return check_recursively(next_x as u32, next_y as u32, dx, dy, next_char, input);
    }
    else if last_char == 'M' && next_char == 'A' {
        return check_recursively(next_x as u32, next_y as u32, dx, dy, next_char, input);
    }
    else if last_char == 'A' && next_char == 'S' {
        return true;
    }
    
    false
}

fn part1(input : &Vec<Vec<char>>) -> u32 {
    let row_count = input.len();
    let col_count = input[0].len();

    let mut ctr = 0;
    for row in 0..row_count {
        for col in 0..col_count {
            if input[row][col] == 'X' {
                DXS.iter().zip(DYS.iter())
                    .for_each(|(dx, dy)| ctr += check_recursively(col as u32, row as u32, *dx, *dy, 'X', input) as u32);
            }
        }
    }

    ctr
}

fn check_cross(x : i32, y : i32, input : &Vec<Vec<char>>) -> bool {
    let min_x = x - 1;
    let min_y = y - 1;
    let max_x = x + 1;
    let max_y = y + 1;

    if min_x < 0 || max_x < 0 || min_x >= input[0].len() as i32 || max_x >= input[0].len() as i32 {
        return false;
    }
    if min_y < 0 || max_y < 0 || min_y >= input.len() as i32 || max_y >= input.len() as i32 {
        return false;
    }

    let upper_left = input[min_y as usize][min_x as usize];
    let upper_right = input[min_y as usize][max_x as usize];
    let lower_left = input[max_y as usize][min_x as usize];
    let lower_right = input[max_y as usize][max_x as usize];

    if !(upper_left == 'M' && lower_right == 'S' || upper_left == 'S' && lower_right == 'M') {
        return false;
    }
    if !(upper_right == 'M' && lower_left == 'S' || upper_right == 'S' && lower_left == 'M') {
        return false;
    }
    
    true
}

fn part2(input : &Vec<Vec<char>>) -> u32 {
    let row_count = input.len();
    let col_count = input[0].len();

    let mut ctr = 0;
    for row in 0..row_count {
        for col in 0..col_count {
            if input[row][col] == 'A' {
                ctr += check_cross(col as i32, row as i32, input) as u32;
            }
        }
    }

    ctr
}

fn main() {
    let input = read_input("src/input.txt");

    let char_vec = input.iter().map(|x| x.chars().collect()).collect();
    println!("Solution 1: {}", part1(&char_vec));
    println!("Solution 2: {}", part2(&char_vec));
}
