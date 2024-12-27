import sys
from avltree import AvlTree
from dataclasses import dataclass

import base


@dataclass
class Node:
    children: dict[str, "Node"]

    def __init__(self):
        self.children = AvlTree[str, Node]({})


@dataclass
class Trie:
    root: Node

    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        current = self.root
        for i, ch in enumerate(word):
            is_last_char = i == len(word) - 1
            try:
                child = current.children[ch]
            except KeyError:
                # Child not present
                child = Node()
                current.children[ch] = child
                if is_last_char:
                    return True
            current = child
        # No new nodes created => already present
        return False

    def contains(self, word: str) -> bool:
        current = self.root
        for ch in word:
            try:
                child = current.children[ch]
                current = child
            except KeyError:
                return False
        return len(current.children) == 0

    def delete(self, word: str) -> bool:
        current = self.root
        parent = None
        key_to_delete = None

        for ch in word:
            try:
                child = current.children[ch]
                parent = current
                key_to_delete = ch
                current = child
            except KeyError:
                return False
        assert parent is not None and key_to_delete is not None
        del parent.children[key_to_delete]
        return True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python balanced-search-tree-trie.py <input_file> <query_file> <output_file>"
        )
    input_file_path = sys.argv[1]
    query_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    base.run(input_file_path, query_file_path, output_file_path, lambda: Trie())
