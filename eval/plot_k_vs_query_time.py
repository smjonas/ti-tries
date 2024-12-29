import sys

import matplotlib.pyplot as plt
import pandas as pd


def plot_query_time(output_file, results_csvs):
    df = pd.concat([pd.read_csv(csv) for csv in results_csvs], ignore_index=True)
    projects = df["project_name"].unique()
    modes = {"insert": "-", "delete": "dotted"}
    colors = plt.cm.tab10.colors

    plt.figure(figsize=(12, 6))

    for i, project in enumerate(projects):
        project_data = df[df["project_name"] == project]
        for mode, linestyle in modes.items():
            mode_data = project_data[project_data["mode"] == mode]
            if not mode_data.empty:
                mode_data = mode_data.sort_values(by="k")
                plt.plot(
                    mode_data["k"],
                    mode_data["query_time"],
                    label=f"{project} - {mode}",
                    linestyle=linestyle,
                    color=colors[i % len(colors)],
                )

    plt.xlabel("Number of Queries (k)")
    plt.ylabel("Query Time (ms)")
    # plt.title("Query Time per k, Grouped by Mode")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(
            "Usage: python plot_k_vs_query_time.py <output_file> <results_csv1> [<results_csv2> ...]"
        )

    output_file = sys.argv[1]
    results_csvs = sys.argv[2:]
    plot_query_time(output_file, results_csvs)
