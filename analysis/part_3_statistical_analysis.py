import matplotlib
import numpy as np

matplotlib.use("Agg")  # non interactive mode
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from scipy.stats import mannwhitneyu
from sqlalchemy.engine import Engine

from load_data import POPULATIONS


def get_group_frequencies(
    all_frequencies: pd.DataFrame, engine: Engine
) -> pd.DataFrame:
    metadata = pd.read_sql(
        """
        SELECT
            sample.id AS sample,
            subject.condition,
            subject.treatment,
            subject.response,
            sample.sample_type
        FROM sample
        JOIN subject ON sample.subject_id = subject.id
        """,
        engine,
    )

    merged = all_frequencies.merge(metadata, on="sample")

    return merged[
        (merged["condition"] == "melanoma")
        & (merged["treatment"] == "miraclib")
        & (merged["sample_type"] == "PBMC")
        & (merged["response"].notna())
    ]


def generate_boxplots(group_frequencies: pd.DataFrame) -> dict[str, Figure]:
    np.random.seed(42)  # Ensures the same plots are created every run
    figures = {}

    for population in POPULATIONS:
        pop_df = group_frequencies[group_frequencies["population"] == population]

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(
            data=pop_df, x="response", y="percentage", order=["no", "yes"], ax=ax
        )
        sns.stripplot(
            data=pop_df,
            x="response",
            y="percentage",
            order=["no", "yes"],
            color="black",
            alpha=0.4,
            size=3,
            ax=ax,
        )
        ax.set_title(f"{population} relative frequency: responders vs non-responders")
        ax.set_xlabel("Response")
        ax.set_ylabel("Relative frequency (%)")

        figures[population] = fig

    return figures


def compute_stats(group_frequencies: pd.DataFrame) -> pd.DataFrame:
    n_tests = len(POPULATIONS)
    rows = []

    for population in POPULATIONS:
        pop_df = group_frequencies[group_frequencies["population"] == population]

        responder_values = pop_df.loc[pop_df["response"] == "yes", "percentage"]
        non_responder_values = pop_df.loc[pop_df["response"] == "no", "percentage"]

        statistic, p_value = mannwhitneyu(
            responder_values, non_responder_values, alternative="two-sided"
        )

        p_value_corrected = min(p_value * n_tests, 1.0)

        rows.append(
            {
                "population": population,
                "n_responders": len(responder_values),
                "n_non_responders": len(non_responder_values),
                "median_responders": round(responder_values.median(), 2),
                "median_non_responders": round(non_responder_values.median(), 2),
                "u_statistic": round(statistic, 2),
                "p_value": round(p_value, 4),
                "p_value_corrected": round(p_value_corrected, 4),
                "significant": p_value_corrected < 0.05,
            }
        )

    return pd.DataFrame(rows)
