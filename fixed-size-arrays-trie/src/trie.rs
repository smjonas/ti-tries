use core::panic;
use std::borrow::BorrowMut;

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
                }
            }
        }
        return current.is_end_of_word;
    }

    // Ensure that this function has a mutable reference to self
    pub fn delete(&mut self, word: &str) -> bool {
        let mut current = &mut self.root;
        let mut parent: Option<&mut Node> = None;
        let mut index_to_delete: Option<usize> = None;

        for ch in word.chars() {
            match char_to_index(ch) {
                None => {
                    return false;
                }
                Some(index) => {
                    // Use `as_mut()` to get a mutable reference to the child node if it exists
                    if let Some(child) = current.children[index].as_mut() {
                        parent = Some(current);
                        index_to_delete = Some(index);
                        current = child;
                    } else {
                        return false;
                    }
                }
            }
        }

        // Ensure that both `parent` and `index_to_delete` are `Some`
        assert!(
            parent.is_some() && index_to_delete.is_some(),
            "Parent or index_to_delete is None"
        );

        // Safely unwrap `parent` and `index_to_delete`
        let parent = parent.unwrap();
        let index_to_delete = index_to_delete.unwrap();

        // Check if all children of the parent node are `None`
        if parent.children.iter().all(|child| child.is_none()) {
            parent.is_end_of_word = true;
        }

        // If needed, uncomment and adjust the following lines:
        // parent.children[index_to_delete].as_mut().unwrap().is_end_of_word = false;
        // current.is_end_of_word = false;

        return true;
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
