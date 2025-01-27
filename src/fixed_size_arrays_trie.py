from dataclasses import dataclass
from typing import Optional

import base


def char_to_index(ch: str) -> Optional[int]:
    if ch == "\0":
        return base.ALPHABET_SIZE - 1
    elif "a" <= ch <= "z":
        return ord(ch) - ord("a")
    elif "A" <= ch <= "Z":
        return ord(ch) - ord("A") + 26
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
    root: Node

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
                    # Create a new child node if none exists for the character.
                    current.children[idx] = Node()
                    child = current.children[idx]
                    # Mark the current node as non-leaf since it now has children.
                    current.is_leaf = False
                    if is_last_char:
                        return True
                current = child
            else:
                raise ValueError(f"Invalid character '{ch}' in word '{word}'")
        # No new nodes created => word is already present in the trie
        return False

    def contains(self, word: str) -> bool:
        current = self.root
        for ch in word:
            idx = char_to_index(ch)
            if idx is None:
                # Return False for unrecognized characters.
                return False
            child = current.children[idx]
            if child is None:
                # Return False if character path does not exist in the trie.
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
                # Return False for unrecognized characters.
                return False
            child = current.children[idx]
            if child is None:
                # Return False if character path does not exist in the trie.
                return False
            parent = current
            idx_to_delete = idx
            current = child
        # parent or idx_to_delete being None here would be a bug.
        assert parent is not None and idx_to_delete is not None
        parent.children[idx_to_delete] = None
        # If the parent has no remaining children, mark it as a leaf.
        if all(child is None for child in parent.children):
            parent.is_leaf = True
        return True
