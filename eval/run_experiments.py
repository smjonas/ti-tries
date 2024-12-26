import run

num_words_max = 1000
step_size = 100
word_length = 10

assert num_words_max % step_size == 0

input_file_path = f"./dataset/trie_n-[[num_words]]_l-{word_length}.txt"
num_words = [step_size + i * step_size for i in range(num_words_max // step_size)]
run.add(
    "gen_dataset",
    f"python3 gen_dataset.py [[num_words]] {word_length} {input_file_path}",
    {"num_words": num_words},
    creates_file=input_file_path,
)

project = "fixed-size-arrays-trie"
run.add(
    "benchmark",
    f"python3 benchmark.py {project} {input_file_path} ../input/empty-queries.txt ../output/tmp-results.txt",
    {"num_words": num_words},
    header_command="python3 benchmark.py --header",
    stdout_file=f"./output/benchmark-results-{project}.csv",
)

run.run()
