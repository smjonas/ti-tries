import os

import run

num_words_max = 1000
step_size = 100
word_length = 10
seed = 42

assert num_words_max % step_size == 0

input_file_path = f"./dataset/trie_n-[[num_words]]_l-{word_length}.txt"
num_words = [step_size + i * step_size for i in range(num_words_max // step_size)]
run.add(
    "gen_dataset",
    f"python3 gen_dataset.py [[num_words]] {word_length} {input_file_path}",
    {"num_words": num_words},
    creates_file=input_file_path,
)

# Experiment 1:
# - words in ascending order
run.group("exp1")
projects = ["fixed-size-arrays-trie", "hash-tables-trie"]
for project in projects:
    run.add(
        f"benchmark-{project}-exp1",
        f"python3 benchmark.py {project} {input_file_path} ./input/empty-queries.txt ./output/tmp-results.txt",
        {"num_words": num_words},
        header_command="python3 benchmark.py --header",
        stdout_file=f"./output/benchmark-results-exp1-{project}.csv",
    )
project_result_files = " ".join(
    [f"./output/benchmark-results-exp1-{project}.csv" for project in projects]
)
run.add(
    "plot-exp1",
    f"python3 plot_n_vs_any.py construction_memory MiB ./output/exp1_n_vs_construction_memory.png {project_result_files}",
    {},
)

# Experiment 2
run.group("exp2")
query_all_words_file_path = f"./input/query_all_{os.path.basename(input_file_path)}"
run.add(
    "gen_query_file",
    f"python3 gen_query_file.py {input_file_path} [[query_all_words_file_name]] {seed}",
    {
        "num_words": num_words,
        "query_all_words_file_name": query_all_words_file_path,
    },
    creates_file=query_all_words_file_path,
)
projects = ["fixed-size-arrays-trie", "hash-tables-trie"]
for project in projects:
    run.add(
        f"benchmark-{project}-exp2",
        f"python3 benchmark.py {project} {input_file_path} {query_all_words_file_path} ./output/tmp-results.txt",
        {"num_words": num_words},
        header_command="python3 benchmark.py --header",
        stdout_file=f"./output/benchmark-results-exp2-{project}.csv",
    )
run.add(
    "plot-exp2",
    "python3 plot_n_vs_any.py ./output/benchmark-results-exp2-{project}.csv query_time ms ./output/exp2_n_vs_query_time.png",
    {},
)

run.run()
