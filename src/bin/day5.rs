use common::read_input;
use std::collections::HashMap;
use std::collections::HashSet;

fn check_valid(update : &String, rule_map : &HashMap<u32, Vec<u32>>) -> bool {
    let mut visited_nums : HashSet<u32> = HashSet::new();
    let mut num_exists : HashSet<u32> = HashSet::new();
    let num_iter = update.split(',');

    num_iter.clone().map(|x| x.parse::<u32>().unwrap())
            .for_each(|x| {num_exists.insert(x);});

    let mut valid = true;
    num_iter.clone().map(|x| x.parse::<u32>().unwrap())
            .for_each(|x| {
                if rule_map.contains_key(&x) {
                    let result = rule_map[&x].iter()
                                             .find(|x| !visited_nums.contains(x) && num_exists.contains(x));

                    if result.is_some() {
                        // this update is not valid
                        valid = false;
                    }
                };

                visited_nums.insert(x);
            });
    valid
}

fn part1(rules : &[String], updates : &[String]) -> u32 {
    // key -> right side of rule, value, list of left sides
    let mut rule_map : HashMap<u32, Vec<u32>> = HashMap::new();
    for rule in rules {
        let (rule_left, rule_right) = rule.split_at(2);
        let index = rule_right[1..].parse::<u32>().unwrap();

        if rule_map.contains_key(&index) {
            rule_map.get_mut(&index).unwrap()
                    .push(rule_left.parse::<u32>().unwrap());
        }
        else {
            let mut new_vec = Vec::new();
            new_vec.push(rule_left.parse::<u32>().unwrap());
            rule_map.insert(index, new_vec);
        }
    }

    let mut acc = 0;
    for update in updates {
        let valid = check_valid(update, &rule_map);

        if valid {
            let num_vec : Vec<u32> = update.split(',').map(|x| x.parse::<u32>().unwrap()).collect();
            acc += num_vec[num_vec.len() / 2];
        }
    }

    acc
}

fn part2(rules : &[String], updates : &[String]) -> u32 {
    // key -> right side of rule, value, list of left sides
    let mut rule_map : HashMap<u32, Vec<u32>> = HashMap::new();
    for rule in rules {
        let (rule_left, rule_right) = rule.split_at(2);
        let index = rule_right[1..].parse::<u32>().unwrap();

        if rule_map.contains_key(&index) {
            rule_map.get_mut(&index).unwrap()
                    .push(rule_left.parse::<u32>().unwrap());
        }
        else {
            let mut new_vec = Vec::new();
            new_vec.push(rule_left.parse::<u32>().unwrap());
            rule_map.insert(index, new_vec);
        }
    }

    let mut acc = 0;
    for update in updates {
        if check_valid(update, &rule_map) {
            continue
        }

        let mut visited_nums : HashSet<u32> = HashSet::new();
        let mut num_exists : HashSet<u32> = HashSet::new();
        let num_iter = update.split(',');

        num_iter.clone().map(|x| x.parse::<u32>().unwrap())
                .for_each(|x| {num_exists.insert(x);});

        let mut num_vec : Vec<u32> = num_iter.map(|x| x.parse::<u32>().unwrap()).collect();

        for i in 0..num_vec.len() {
            if !rule_map.contains_key(&num_vec[i]) {
                continue
            }

            loop {
                let mut conflict_num = -1;

                rule_map.get(&num_vec[i]).unwrap().iter()
                        .for_each(|left| {
                            if !visited_nums.contains(&left) && num_exists.contains(left) {
                                conflict_num = *left as i32;
                            }
                        });

                if conflict_num != -1 {
                    let j = num_vec.iter().position(|x| *x == conflict_num as u32).unwrap();
                    let temp = num_vec[i];
                    num_vec[i] = num_vec[j];
                    num_vec[j] = temp;
                }
                else {
                    break
                }
            }

            visited_nums.insert(num_vec[i]);
        }

        acc += num_vec[num_vec.len()/2]
    }

    acc
}

fn main() {
    let input = read_input("src/input.txt");
    let mut input_iter = input.split(|x| x == "");

    let rules = input_iter.next().unwrap();
    let updates = input_iter.next().unwrap();

    println!("Solution 1: {}", part1(rules, updates));
    println!("Solution 2: {}", part2(rules, updates));
}
