import sys
from dataclasses import dataclass
from typing import Optional

# a-z, A-Z, 0-9, null byte
ALPHABET_SIZE = 26 + 26 + 10 + 1


def char_to_index(ch: str) -> Optional[int]:
    if ch == "\0":
        return ALPHABET_SIZE - 1
    elif "A" <= ch <= "Z":
        return ord(ch) - ord("A")
    elif "a" <= ch <= "z":
        return ord(ch) - ord("a") + 26
    elif "0" <= ch <= "9":
        return ord(ch) - ord("0") + 26 + 26
    else:
        return None


@dataclass
class Node:
    children: list[Optional["Node"]]
    is_eow: bool

    def __init__(self):
        self.children = [None] * ALPHABET_SIZE
        self.is_eow = True


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
                    current.children[idx] = Node()
                    child = current.children[idx]
                    current.is_eow = False
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
        return current.is_eow

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
            parent.is_eow = True
        return True


if __name__ == "__main__":
    input_file_path = sys.argv[1]
    query_file_path = sys.argv[2]
    with open(input_file_path, "r") as input_file:
        input_contents = input_file.read()
    input_words = [word for word in input_contents.split("\n") if word != ""]
    print(input_words)
    trie = Trie()
    for word in input_words:
        trie.insert(word)
    with open(query_file_path, "r") as query_file:
        query_contents = query_file.read()
    query_lines = query_contents.split("\n")
    for query_line in query_lines:
        if query_line == "":
            continue
        query_word, query_type = query_line.split(" ")
        match query_type:
            case "i":
                print(trie.insert(query_word))
            case "c":
                print(trie.contains(query_word))
            case "d":
                print(trie.delete(query_word))
            case _:
                raise ValueError(f"Invalid query type '{query_type}'")
    print(query_lines)
