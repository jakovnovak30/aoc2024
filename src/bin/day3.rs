use common::read_input;

fn part1(input : &str) -> u32 {
    let mut last_char = '0';
    let mut x = 0;
    let mut y = 0;
    let mut result = 0;

    for char in input.chars() {
        if last_char == '0' && char == 'm' {
            last_char = 'm'
        }
        else if last_char == 'm' && char == 'u' {
            last_char = 'u'
        }
        else if last_char == 'u' && char == 'l' {
            last_char = 'l'
        }
        else if last_char == 'l' && char == '(' {
            last_char = '('
        }
        else if last_char == '(' && char.is_digit(10) {
            x = char.to_digit(10).unwrap();
            last_char = 'X'
        }
        else if last_char == 'X' && char.is_digit(10) {
            x = char.to_digit(10).unwrap() + x*10;
            last_char = 'X'
        }
        else if last_char == 'X' && char == ',' {
            last_char = ','
        }
        else if last_char == ',' && char.is_digit(10) {
            y = char.to_digit(10).unwrap();
            last_char = 'Y'
        }
        else if last_char == 'Y' && char.is_digit(10) {
            y = char.to_digit(10).unwrap() + y*10;
            last_char = 'Y'
        }
        else if last_char == 'Y' && char == ')' {
            result += x*y;
            last_char = '0'
        }
        else {
            last_char = '0'
        }
    }

    result
}

fn part2(input : &str) -> u32 {
    let mut last_char = '0';
    let mut x = 0;
    let mut y = 0;
    let mut result = 0;
    let mut enabled = true;

    for char in input.chars() {
        if char == 'm' {
            last_char = 'm'
        }
        else if last_char == 'm' && char == 'u' {
            last_char = 'u'
        }
        else if last_char == 'u' && char == 'l' {
            last_char = 'l'
        }
        else if last_char == 'l' && char == '(' {
            last_char = '('
        }
        else if last_char == '(' && char.is_digit(10) {
            x = char.to_digit(10).unwrap();
            last_char = 'X'
        }
        else if last_char == 'X' && char.is_digit(10) {
            x = char.to_digit(10).unwrap() + x*10;
            last_char = 'X'
        }
        else if last_char == 'X' && char == ',' {
            last_char = ','
        }
        else if last_char == ',' && char.is_digit(10) {
            y = char.to_digit(10).unwrap();
            last_char = 'Y'
        }
        else if last_char == 'Y' && char.is_digit(10) {
            y = char.to_digit(10).unwrap() + y*10;
            last_char = 'Y'
        }
        else if last_char == 'Y' && char == ')' {
            if enabled {
                result += x*y
            }
            last_char = '0'
        }
        // Do/don't logic
        else if char == 'd' {
            last_char = 'd'
        }
        else if last_char == 'd' && char == 'o' {
            last_char = 'o'
        }
        else if last_char == 'o' && char == '(' {
            last_char = '1' // because '(' is alredy taken
        }
        else if last_char == '1' && char == ')' {
            enabled = true;
            last_char = '0'
        }
        else if last_char == 'o' && char == 'n' {
            last_char = 'n';
        }
        else if last_char == 'n' && char == '\'' {
            last_char = '\''
        }
        else if last_char == '\'' && char == 't' {
            last_char = 't'
        }
        else if last_char == 't' && char == '(' {
            last_char = '2'
        }
        else if last_char == '2' && char == ')' {
            enabled = false;
            last_char = '0'
        }
        else {
            last_char = '0'
        }
    }

    result
}

fn main() {
    let input = &read_input("src/input.txt")[0];

    println!("Solution 1: {}", part1(input));
    println!("Solution 2: {}", part2(input));
}
