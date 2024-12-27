import string
import sys
from itertools import islice, product
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python gen_dataset.py <num_words> <word_length> <trie_file_path>"
        )

    num_words = int(sys.argv[1])
    word_length = int(sys.argv[2])
    trie_file_path = sys.argv[3]

    # Generate sorted words
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

    def generate_words():
        for word in product(characters, repeat=word_length - 1):
            yield "".join(str(ch) for ch in word) + "\0"

    sorted_words = list(islice(generate_words(), num_words))

    Path(trie_file_path).parent.mkdir(exist_ok=True, parents=True)
    with open(trie_file_path, "w") as file:
        for word in sorted_words:
            file.write(word + "\n")
