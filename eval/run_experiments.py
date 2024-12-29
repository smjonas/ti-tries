import os

import run

num_words_max = 1000
words_step_size = 100
word_length = 10

queries_step_size = 100

seed = 42

assert num_words_max % words_step_size == 0
num_words = [(i + 1) * words_step_size for i in range(num_words_max // words_step_size)]
input_file_path = f"./dataset/trie_n-[[num_words]]_l-{word_length}.txt"
run.add(
    "gen-dataset",
    f"python3 gen_dataset.py [[num_words]] {word_length} {input_file_path}",
    {"num_words": num_words},
    creates_file=input_file_path,
)

# Experiment 1:
# - words in ascending order
run.group("exp1")
projects = [
    "fixed-size-arrays-trie",
    "hash-tables-trie",
    "balanced-search-tree-trie",
]
for project in projects:
    run.add(
        f"benchmark-{project}-exp1",
        f"python3 benchmark.py {project} {input_file_path} ./queries/empty-queries.txt ./output/tmp-results.txt",
        {"num_words": num_words},
        header_command="python3 benchmark.py --header",
        stdout_file=f"./output/benchmark-results-exp1-{project}.csv",
    )
project_result_files_exp1 = " ".join(
    [f"./output/benchmark-results-exp1-{project}.csv" for project in projects]
)
run.add(
    "plot-exp1",
    f'python3 plot.py n "Number of Words" construction_memory MiB ./output/exp1_n_vs_construction_memory.png {project_result_files_exp1}',
    {},
)

# Experiment 2
run.group("exp2")
query_contains_all_file_path = (
    f"./queries/contains/contains_all_{os.path.basename(input_file_path)}"
)
run.add(
    "gen-query-file",
    f"python3 gen_query_file.py {input_file_path} [[query_contains_all_file_path]] {seed}",
    {
        "num_words": num_words,
        "query_contains_all_file_path": query_contains_all_file_path,
    },
    creates_file=query_contains_all_file_path,
)
for project in projects:
    run.add(
        f"benchmark-{project}-exp2",
        f"python3 benchmark.py {project} {input_file_path} {query_contains_all_file_path} ./output/tmp-results.txt",
        {"num_words": num_words},
        header_command="python3 benchmark.py --header",
        stdout_file=f"./output/benchmark-results-exp2-{project}.csv",
    )
project_result_files_exp2 = " ".join(
    [f"./output/benchmark-results-exp2-{project}.csv" for project in projects]
)
run.add(
    "plot-exp2",
    f'python3 plot.py n "Number of Words" query_time ms ./output/exp2_n_vs_query_time.png {project_result_files_exp2}',
    {},
)

# Experiment 3
run.group("exp3")
assert num_words_max % queries_step_size == 0
num_queries = [
    (i + 1) * queries_step_size for i in range(num_words_max // queries_step_size)
]
input_file_path = f"./dataset/trie_n-{num_words_max}_l-{word_length}.txt"
for mode in ["insert", "delete"]:
    query_file_path = (
        f"./queries/{mode}/{mode}_k-[[num_queries]]_{os.path.basename(input_file_path)}"
    )
    run.add(
        f"gen-{mode}-query-file",
        f"python3 gen_insert_delete_dataset.py {input_file_path} {mode} [[num_queries]] {query_file_path} {seed}",
        {"num_queries": num_queries},
        creates_file=query_file_path,
    )

project_result_files_exp3 = []
for project in projects:
    exp3_results_file = f"./output/benchmark-results-exp3-{project}.csv"
    run.add(
        f"benchmark-{project}-exp3",
        f"python3 benchmark.py {project} {input_file_path} {query_file_path} ./output/tmp-results.txt",
        {"num_queries": num_queries},
        header_command="python3 benchmark.py --header",
        stdout_file=exp3_results_file,
    )
    project_result_files_exp3.append(exp3_results_file)
run.add(
    "plot-exp3",
    f'python3 plot.py k "Number of Queries" query_time ms ./output/exp3_k_vs_query_time.png {" ".join(project_result_files_exp3)}',
    {},
)

run.run()
