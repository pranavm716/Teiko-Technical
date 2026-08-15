import os

import matplotlib.pyplot as plt
import pandas as pd

from analysis.part_2_frequencies import compute_frequencies
from analysis.part_3_statistical_analysis import (
    compute_stats,
    generate_boxplots,
    get_group_frequencies,
)
from analysis.part_4_data_subset_analysis import (
    compute_average_b_cells_melanoma_male_responders,
    get_baseline_samples,
    summarize_baseline_breakdown,
)
from db.engine import engine

OUTPUT_DIR = "output"
BOXPLOTS_DIR = f"{OUTPUT_DIR}/part_3_boxplots"
SUBSETS_DIR = f"{OUTPUT_DIR}/part_4_subsets"


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


def save_part_4_data_subset_analysis_output() -> None:
    baseline_samples = get_baseline_samples(engine)
    baseline_samples.to_csv(f"{OUTPUT_DIR}/part_4_baseline_samples.csv", index=False)

    breakdowns = summarize_baseline_breakdown(baseline_samples)
    os.makedirs(SUBSETS_DIR, exist_ok=True)
    for name, breakdown_df in breakdowns.items():
        breakdown_df.to_csv(f"{SUBSETS_DIR}/{name}.csv", index=False)

    avg_b_cells = compute_average_b_cells_melanoma_male_responders(engine)
    pd.DataFrame([{"avg_b_cells_melanoma_male_responders": avg_b_cells}]).to_csv(
        f"{OUTPUT_DIR}/part_4_average_b_cells_responders.csv", index=False
    )
    print(
        f"run_analysis.py: average B cells for melanoma male responders at time=0: {avg_b_cells:.2f}"
    )

    print("run_analysis.py: part 4 baseline subset and breakdowns written")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_frequencies = compute_frequencies(engine)
    save_part_2_frequencies_output(all_frequencies)
    save_part_3_statistical_analysis_output(all_frequencies)
    save_part_4_data_subset_analysis_output()


if __name__ == "__main__":
    main()
