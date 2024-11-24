import resource
import sys
import time
from dataclasses import dataclass
from typing import Optional

# a-z, A-Z, 0-9, null byte
ALPHABET_SIZE = 26 + 26 + 10 + 1


def char_to_index(ch: str) -> Optional[int]:
    if ch == "\0":
        return ALPHABET_SIZE - 1
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
        self.children = [None] * ALPHABET_SIZE
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
    input_file_path = sys.argv[1]
    query_file_path = sys.argv[2]
    with open(input_file_path, "r") as input_file:
        input_contents = input_file.read()
    with open(query_file_path, "r") as query_file:
        query_contents = query_file.read()
    output_file_path = f"result_{input_file_path.split('/')[-1]}"
    input_words = input_contents.split("\n")[:-1]
    query_lines = query_contents.split("\n")[:-1]

    start_time = time.time()
    trie = Trie()
    for word in input_words:
        trie.insert(word)
    trie_construction_time_end = time.time()

    results = []
    for query_line in query_lines:
        query_word, query_type = query_line.split(" ")
        match query_type:
            case "i":
                results.append(trie.insert(query_word))
            case "c":
                results.append(trie.contains(query_word))
            case "d":
                results.append(trie.delete(query_word))
            case _:
                raise ValueError(f"Invalid query type '{query_type}'")

    query_time_end = time.time()
    with open(output_file_path, "w") as output_file:
        for result in results:
            output_file.write(("true" if result else "false") + "\n")
    trie_construction_time_ms = (trie_construction_time_end - start_time) * 1000
    query_time_ms = (query_time_end - start_time) * 1000
    trie_construction_memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Convert kilobytes to mebibytes
    trie_construction_memory_mib = (trie_construction_memory_kb * 1000) / 1_048_576
    print(
        f"RESULT name=Jonas-Strittmatter trie_construction_time={trie_construction_time_ms:.4f} "
        f"trie_construction_memory={trie_construction_memory_mib:.4f} query_time={query_time_ms:.4f}"
    )
