import re
import subprocess
import sys


def parse_result(result_string: str, pattern: str) -> dict:
    matches = re.findall(pattern, result_string)
    values = {}
    for key, value in matches:
        values[key] = value
    return values


def benchmark_project(project_name, input_file, query_file, output_file):
    command = (
        f"python3 ../src/{project_name}.py {input_file} {query_file} {output_file}"
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(result.stderr)
    return parse_result(result.stdout, r"(\w+)=([\d.]+)")


def print_result(project_name, input_file, query_file, output_file):
    input_params = parse_result(input_file, r"(\w)-([\d.]+)")
    query_params = parse_result(query_file, r"(\w)-([\d.a-z]+)")
    mode, k, n, l = (
        query_params.get("m", "-"),
        query_params.get("k", "-"),
        input_params["n"],
        input_params["l"],
    )
    results = benchmark_project(project_name, input_file, query_file, output_file)
    construction_time, construction_memory, query_time = (
        results["trie_construction_time"],
        results["trie_construction_memory"],
        results["query_time"],
    )
    print(
        f"{project_name},{n},{l},{k},{mode},{input_file},{query_file},{construction_time},{construction_memory},{query_time}"
    )


def print_header():
    print(
        "project_name,n,l,k,mode,input_file,query_file,construction_time,construction_memory,query_time"
    )


if __name__ == "__main__":
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    flags = [arg for arg in sys.argv[1:] if arg.startswith("--")]
    if "--header" in flags:
        print_header()
        sys.exit(0)

    if len(sys.argv) != 5:
        sys.exit(
            "Usage: python <project_name> <input_file> <query_file> <output_file> [--header]"
        )

    print_result(*args)
