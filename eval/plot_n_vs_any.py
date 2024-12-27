import sys

import matplotlib.pyplot as plt
import pandas as pd


def plot_results(result_csvs: list[str], y_column, y_column_unit, output_path):
    df = pd.concat([pd.read_csv(csv) for csv in result_csvs], ignore_index=True)
    projects = df["project_name"].unique()
    colors = plt.cm.tab20.colors

    plt.figure(figsize=(12, 6))
    for project, color in zip(projects, colors):
        subset = df[df["project_name"] == project]
        plt.scatter(subset["n"], subset[y_column], label=f"{project}", color=color)

    plt.xlim(0)
    # plt.ylim(0)
    plt.xlabel("Number of Words")
    plt.ylabel(f"{y_column.replace('_', ' ').title()} ({y_column_unit})")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit(
            "Usage: python plot_n_vs_time_or_space.py <y_column> <y_column_unit> <output_path> <results_csv_1> [<results_csv_2> ...]"
        )

    y_column = sys.argv[1]
    y_column_unit = sys.argv[2]
    output_path = sys.argv[3]
    result_csvs = sys.argv[4:]
    plot_results(result_csvs, y_column, y_column_unit, output_path)
