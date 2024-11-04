const ALPHABET_SIZE: usize = 26 + 26 + 10;

#[derive(Debug)]
pub struct Node {
    pub children: [Option<Box<Node>>; ALPHABET_SIZE],
    pub is_end_of_word: bool,
}

impl Node {
    pub fn new() -> Node {
        Node { children: std::array::from_fn(|_| None), is_end_of_word: false }
    }
}
