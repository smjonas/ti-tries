use core::panic;

use crate::node::Node;

#[derive(Debug)]
pub struct Trie {
    root: Node,
}

impl Trie {
    pub fn new() -> Trie {
        Trie { root: Node::new() }
    }

    pub fn insert(&mut self, word: &str) {
        let mut current = &mut self.root;
        for ch in word.chars() {
            if let Some(index) = char_to_index(ch) {
                current = current.children[index].get_or_insert_with(|| Box::new(Node::new()))
            } else {
                panic!("Invalid character '{}' in word '{}'", ch, word);
            }
        }
    }

    pub fn contains(&self, word: &str) -> bool {
        let mut current = &self.root;
        for ch in word.chars() {
            match char_to_index(ch) {
                None => {
                    return false;
                }
                Some(index) => {
                    if let Some(child) = &current.children[index] {
                        current = child.as_ref();
                    } else {
                        return false;
                    }
                },
            }
        }
        return current.is_end_of_word;
    }
}

fn char_to_index(c: char) -> Option<usize> {
    match c {
        'A'..='Z' => Some((c as usize) - ('A' as usize)),
        'a'..='z' => Some((c as usize) - ('a' as usize) + 26),
        '0'..='9' => Some((c as usize) - ('0' as usize) + 26 + 26),
        _ => None,
    }
}
