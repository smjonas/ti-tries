import sys

import matplotlib.pyplot as plt
import pandas as pd


def plot_results(
    results_csvs: list[str],
    x_column,
    x_column_label,
    y_column,
    y_column_unit,
    output_path,
):
    # Combine multiple CSVs into a single DataFrame
    df = pd.concat([pd.read_csv(csv) for csv in results_csvs], ignore_index=True)
    projects = df["project_name"].unique()
    colors = plt.cm.tab20.colors

    plt.figure(figsize=(12, 6))
    for project, color in zip(projects, colors):
        subset = df[df["project_name"] == project]
        plt.scatter(subset[x_column], subset[y_column], label=f"{project}", color=color)

    plt.xlim(0)
    # plt.ylim(0)
    plt.xlabel(x_column_label)
    plt.ylabel(f"{y_column.replace('_', ' ').title()} ({y_column_unit})")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit(
            "Usage: python plot.py <x_column> <x_column_label> <y_column> <y_column_unit> <output_path> <results_csv1> [<results_csv2> ...]"
        )

    x_column = sys.argv[1]
    x_column_label = sys.argv[2]
    y_column = sys.argv[3]
    y_column_unit = sys.argv[4]
    output_path = sys.argv[5]
    results_csvs = sys.argv[6:]
    plot_results(
        results_csvs, x_column, x_column_label, y_column, y_column_unit, output_path
    )
