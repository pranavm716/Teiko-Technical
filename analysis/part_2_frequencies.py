import pandas as pd
from sqlalchemy.engine import Engine

from load_data import POPULATIONS


def compute_frequencies(engine: Engine) -> pd.DataFrame:
    cell_counts = pd.read_sql(
        "SELECT sample_id AS sample, population, count FROM cell_count",
        engine,
    )

    cell_counts["total_count"] = cell_counts.groupby("sample")["count"].transform("sum")
    cell_counts["percentage"] = (
        cell_counts["count"] / cell_counts["total_count"] * 100
    ).round(2)

    #  Grouping by sample
    cell_counts["population"] = pd.Categorical(
        cell_counts["population"], categories=POPULATIONS, ordered=True
    )
    cell_counts = cell_counts.sort_values(["sample", "population"]).reset_index(
        drop=True
    )

    return cell_counts[["sample", "total_count", "population", "count", "percentage"]]
