import sys

import matplotlib.pyplot as plt
import pandas as pd


def plot_results(results_csv, y_column, y_column_unit, output_path):
    df = pd.read_csv(results_csv)
    projects = df["project_name"].unique()
    colors = plt.cm.tab10.colors

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
    if len(sys.argv) != 5:
        sys.exit(
            "Usage: python plot_n_vs_time_or_space.py <results_csv> <y_column> <y_column_unit> <output_path>"
        )

    results_csv = sys.argv[1]
    y_column = sys.argv[2]
    y_column_unit = sys.argv[3]
    output_path = sys.argv[4]
    plot_results(results_csv, y_column, y_column_unit, output_path)
