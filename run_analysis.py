import os

import matplotlib.pyplot as plt
import pandas as pd

from analysis.part_2_frequencies import compute_frequencies
from analysis.part_3_statistical_analysis import (
    compute_stats,
    generate_boxplots,
    get_group_frequencies,
)
from db.engine import engine

OUTPUT_DIR = "output"
BOXPLOTS_DIR = f"{OUTPUT_DIR}/part_3_boxplots"


def save_part_2_frequencies_output(all_frequencies: pd.DataFrame) -> None:
    all_frequencies.to_csv(f"{OUTPUT_DIR}/part_2_frequencies.csv", index=False)
    print("run_analysis.py: part 2 frequencies written")


def save_part_3_statistical_analysis_output(all_frequencies: pd.DataFrame) -> None:
    group_frequencies = get_group_frequencies(all_frequencies, engine)
    boxplots = generate_boxplots(group_frequencies)

    os.makedirs(BOXPLOTS_DIR, exist_ok=True)
    for population, fig in boxplots.items():
        fig.savefig(f"{BOXPLOTS_DIR}/{population}.png", bbox_inches="tight")
        plt.close(fig)

    print("run_analysis.py: part 3 boxplots written")

    stats_summary = compute_stats(group_frequencies)
    stats_summary.to_csv(f"{OUTPUT_DIR}/part_3_stats_summary.csv", index=False)
    print("run_analysis.py: part 3 stats summary written")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_frequencies = compute_frequencies(engine)
    save_part_2_frequencies_output(all_frequencies)
    save_part_3_statistical_analysis_output(all_frequencies)


if __name__ == "__main__":
    main()
