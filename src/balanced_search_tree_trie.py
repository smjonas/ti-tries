from dataclasses import dataclass
from typing import Optional

from avltree import AvlTree


@dataclass
class Node:
    # Use an AVL tree (a self-balancing binary search tree)
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
            child = current.children.get(ch)
            if child is None:
                # Create a new child node if the character is not present.
                child = Node()
                current.children[ch] = child
                current.is_leaf = False
                # Word inserted successfully.
                if is_last_char:
                    return True
            current = child
        # No new nodes created => the word was already present in the trie.
        return False

    def contains(self, word: str) -> bool:
        current = self.root
        for ch in word:
            if current.children is None:
                # Leaf reached before the last character => not present.
                return False
            child = current.children.get(ch)
            if child is None:
                # Return False if character path does not exist in the trie.
                return False
            current = child
        # A word exists if the final node is a leaf.
        return current.is_leaf

    def delete(self, word: str) -> bool:
        # To track nodes and indices for backtracking.
        stack = []
        current = self.root

        for ch in word:
            if current.children is None:
                return False
            stack.append((current, ch))
            current = current.children.get(ch)
            if current is None:
                return False

        if current.children is not None and len(current.children) > 0:
            # Not a leaf node.
            return False

        # Backtrack and delete nodes if they are no longer needed.
        while stack:
            parent, ch = stack.pop()
            del parent.children[ch]
            if parent.children is not None and len(parent.children) > 0:
                # Stop if the parent still has other children.
                break
            # Remove the AVLTree if it's empty now.
            parent.children = None

        return True
