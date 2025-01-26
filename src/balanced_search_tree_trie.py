from dataclasses import dataclass
from typing import Optional

from avltree import AvlTree


@dataclass
class Node:
    children: Optional[AvlTree[str, "Node"]]
    is_leaf: bool

    def __init__(self):
        self.children = None
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
            if current.children is None:
                current.children = AvlTree[str, Node]()
            try:
                child = current.children[ch]
            except KeyError:
                child = Node()
                current.children[ch] = child
                current.is_leaf = False
                if is_last_char:
                    return True
            current = child
        return False

    def contains(self, word: str) -> bool:
        current = self.root
        for ch in word:
            if current.children is None:
                return False
            try:
                child = current.children[ch]
                current = child
            except KeyError:
                return False
        return current.is_leaf

    def delete(self, word: str) -> bool:
        stack = []  # To track nodes and indices for backtracking
        current = self.root

        for ch in word:
            if current.children is None:
                return False
            try:
                stack.append((current, ch))
                current = current.children[ch]
            except KeyError:
                return False

        if current.children is not None and len(current.children) > 0:
            return False  # Not a leaf node

        # Backtrack and delete nodes if they are no longer needed
        for parent, ch in reversed(stack):
            assert parent.children is not None and ch in parent.children
            del parent.children[ch]
            if len(parent.children) > 0:
                break
            # Remove empty AvlTree
            parent.children = None
        return True
