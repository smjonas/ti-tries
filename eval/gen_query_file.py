import random
import sys


def gen_query_file(input_file: str, output_file: str, query_type: str):
    with open(input_file, "r") as infile:
        lines = infile.readlines()
    random.shuffle(lines)
    lines = list(map(lambda line: f"{line[:-1]} {query_type}\n", lines))
    with open(output_file, "w") as outfile:
        outfile.writelines(lines)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python gen_query_file.py <input_file> <output_query_file> <seed>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_query_file = sys.argv[2]
    seed = int(sys.argv[3])
    random.seed(seed)
    gen_query_file(input_file, output_query_file, "c")
