import os
import resource
import sys
import time
from pathlib import Path
from typing import Callable

import balanced_search_tree_trie
import fixed_size_arrays_trie
import hash_tables_trie

# a-z, A-Z, 0-9, null byte
ALPHABET_SIZE = 26 + 26 + 10 + 1


def run(
    variant, input_file_path, query_file_path, output_file_path, build_trie: Callable
):
    with open(input_file_path, "r") as input_file:
        input_contents = input_file.read()
    with open(query_file_path, "r") as query_file:
        query_contents = query_file.read()
    input_words = input_contents.split("\n")[:-1]
    query_lines = query_contents.split("\n")[:-1]

    start_time = time.time()
    trie = build_trie()
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
        f"RESULT name=Jonas-Strittmatter trie_variant={variant} trie_construction_time={trie_construction_time_ms:.4f} "
        f"trie_construction_memory={trie_construction_memory_mib:.4f} query_time={query_time_ms:.4f}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: python base.py <variant> <input_file> <query_file>")
    variant_str = sys.argv[1]
    try:
        variant = int(variant_str)
        if variant < 1 or variant > 3:
            raise ValueError()
    except ValueError:
        sys.exit("Usage: <variant> must be an integer between 1 and 3")
    input_file_path = sys.argv[2]
    query_file_path = sys.argv[3]
    input_file_name = Path(input_file_path).stem
    output_file_path = os.path.join(
        Path(input_file_path).parent, f"result_{input_file_name}.txt"
    )
    variant_map = {
        1: fixed_size_arrays_trie,
        2: hash_tables_trie,
        3: balanced_search_tree_trie,
    }
    run(
        variant,
        input_file_path,
        query_file_path,
        output_file_path,
        lambda: variant_map[variant].Trie(),
    )
