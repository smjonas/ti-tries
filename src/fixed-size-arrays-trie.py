import sys
from dataclasses import dataclass
from typing import Optional

import base


def char_to_index(ch: str) -> Optional[int]:
    if ch == "\0":
        return base.ALPHABET_SIZE - 1
    elif "a" <= ch <= "z":
        return ord(ch) - ord("A")
    elif "A" <= ch <= "Z":
        return ord(ch) - ord("a") + 26
    elif "0" <= ch <= "9":
        return ord(ch) - ord("0") + 26 + 26
    else:
        return None


@dataclass
class Node:
    children: list[Optional["Node"]]
    is_leaf: bool

    def __init__(self):
        self.children = [None] * base.ALPHABET_SIZE
        self.is_leaf = True


@dataclass
class Trie:
    root: base.Node

    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        current = self.root
        for i, ch in enumerate(word):
            is_last_char = i == len(word) - 1
            idx = char_to_index(ch)
            if idx is not None:
                child = current.children[idx]
                if child is None:
                    current.children[idx] = Node()
                    child = current.children[idx]
                    current.is_leaf = False
                    if is_last_char:
                        return True
                current = child
            else:
                raise ValueError(f"Invalid character '{ch}' in word '{word}'")
        # No new nodes created => already present
        return False

    def contains(self, word: str) -> bool:
        current = self.root
        for ch in word:
            idx = char_to_index(ch)
            if idx is None:
                return False
            child = current.children[idx]
            if child is None:
                return False
            current = child
        return current.is_leaf

    def delete(self, word: str) -> bool:
        current = self.root
        parent = None
        idx_to_delete = None

        for ch in word:
            idx = char_to_index(ch)
            if idx is None:
                return False
            child = current.children[idx]
            if child is None:
                return False
            parent = current
            idx_to_delete = idx
            current = child
        assert parent is not None and idx_to_delete is not None
        parent.children[idx_to_delete] = None
        # Parent only has empty children
        if all(child is None for child in parent.children):
            parent.is_leaf = True
        return True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python fixed-size-arrays-trie.py <input_file> <query_file> <output_file>"
        )
    input_file_path = sys.argv[1]
    query_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    base.run(input_file_path, query_file_path, output_file_path, lambda: Trie())
