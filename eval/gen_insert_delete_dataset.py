import random
import sys


# Creates insert queries from num_queries random trie_words
def get_insert_queries(trie_words, num_queries):
    num_words = len(trie_words)
    if num_queries > num_words:
        raise ValueError(f"num_queries must be at most {num_words}, is {num_queries}")
    random_trie_words = random.choices(trie_words, k=num_queries)
    return list(map(lambda query_word: query_word[:-1] + " i", random_trie_words))


# Creates delete queries from num_queries that are not already in the trie
def get_delete_queries(trie_words, num_queries):
    num_words = len(trie_words)
    if num_queries > num_words:
        raise ValueError(f"num_queries must be at most {num_words}, is {num_queries}")
    random_trie_words = random.choices(trie_words, k=num_queries)
    # Make each word one character longer to cause a cache miss on deletion
    return list(map(lambda query_word: query_word[:-2] + "X\0 d", random_trie_words))


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit(
            "Usage: python gen_insert_delete_dataset.py <trie_file_path> [insert|delete] <num_queries> <query_file_path> <seed>"
        )

    trie_file_path, mode, num_queries, query_file_path, seed = sys.argv[1:]
    num_queries = int(num_queries)
    random.seed(seed)
    with open(trie_file_path, "r") as trie_file:
        trie_words = trie_file.readlines()

    match mode:
        case "insert":
            queries = get_insert_queries(trie_words, num_queries)
        case "delete":
            queries = get_delete_queries(trie_words, num_queries)
        case _:
            sys.exit("Usage: mode must either be insert or delete")

    with open(query_file_path, "w+") as query_file:
        for query in queries:
            query_file.write(query + "\n")
