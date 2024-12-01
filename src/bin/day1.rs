use common::read_input;

fn main() {
    println!("Hello, world!");

    let input = read_input("src/example.txt");

    let mut list1 : Vec<_> = input.clone().into_iter()
                     .map(|x| x.split_whitespace().collect::<Vec<_>>()[0].parse::<i32>().unwrap())
                     .collect();

    let mut list2 : Vec<_> = input.into_iter()
                    .map(|x| x.split_whitespace().collect::<Vec<_>>()[1].parse::<i32>().unwrap())
                    .collect();

    list1.sort();
    list2.sort();

    // PART 1
    let result : i32 = list1.iter().zip(list2.iter())
                    .map(|(x, y)| (x - y).abs())
                    .sum();

    println!("{}", result);

    // PART 2
    let result2 : i32 = list1.iter()
                    .map(|x| x * (list2.clone().into_iter().filter(|y| y == x).count() as i32))
                    .sum();
    println!("{}", result2);
}
