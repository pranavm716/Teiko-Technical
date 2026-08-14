import matplotlib

matplotlib.use("Agg")  # non interactive mode
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
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
