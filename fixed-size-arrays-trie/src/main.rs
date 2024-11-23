mod node;
mod trie;

use trie::Trie;

fn main() {
    // Parse command line arguments
    let args: Vec<String> = std::env::args().collect();
    let input_file_path = &args[1];
    let query_file_path = &args[2];
    let input_contents = std::fs::read_to_string(input_file_path).expect("Failed to read input file");
    let input_words = input_contents.split("\0\n");
    println!("{:?}", input_words);
    let mut trie = Trie::new();
    for word in input_words {
        trie.insert(word);
    }
    println!("{:#?}", trie);
    let query_contents = std::fs::read_to_string(query_file_path).expect("Failed to read query file");
}
