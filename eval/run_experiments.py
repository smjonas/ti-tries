import run

num_words = 1000
word_length = 10

run.add(
    "gen_dataset",
    f"python3 gen_dataset.py {num_words} {word_length} ./dataset/trie_n-{num_words}_l-{word_length}.txt",
    {},
    creates_file=f"./dataset/trie_n-{num_words}_l-{word_length}.txt",
)

run.run()
