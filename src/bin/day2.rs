use common::read_input;

fn is_safe(report : &str) -> bool{
    let numbers : Vec<i32> = report.split_whitespace()
                    .map(|x| x.parse::<i32>().unwrap())
                    .collect();
    let ascending = numbers[1] > numbers[0];

    let mut last_num = numbers[0];

    for number in &numbers[1..] {
        if ascending {
            if *number < last_num {
                return false
            }
        }
        else {
            if *number > last_num {
                return false
            }
        }

        let diff = (*number - last_num).abs();
        if diff > 3 || diff < 1 {
            return false
        }

        last_num = *number;
    }

    true
}

fn is_safe2(report : &str) -> bool{
    let numbers : Vec<i32> = report.split_whitespace()
                    .map(|x| x.parse::<i32>().unwrap())
                    .collect();
    let mut good_iteration = false;

    for ignore_index in 0..numbers.len() {
        let curr_nums : Vec<_> =  numbers[..ignore_index].iter()
            .chain(&numbers[ignore_index+1..])
            .cloned()
            .collect();
            
        let ascending = curr_nums[1] > curr_nums[0];
        let mut last_num = curr_nums[0];
        let mut safe = true;

        for number in &curr_nums[1..] {
            if ascending {
                if *number < last_num {
                    safe = false;
                    break
                }
            }
            else {
                if *number > last_num {
                    safe = false;
                    break
                }
            }

            let diff = (*number - last_num).abs();
            if diff > 3 || diff < 1 {
                safe = false;
                break
            }

            last_num = *number;
        }

        if safe {
            good_iteration = true
        }
    }

    good_iteration
}

fn main() {
    let input = read_input("src/example.txt");

    // PART 1
    let solution1 = input.iter()
                    .filter(|x| is_safe(x))
                    .count();

    println!("Solution 1: {}", solution1);

    // PART 2
    let solution2 = input.iter()
                    .filter(|x| is_safe2(x))
                    .count();

    println!("Solution 1: {}", solution2);
}
