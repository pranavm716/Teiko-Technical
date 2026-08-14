import pandas as pd
from sqlalchemy.engine import Engine


def compute_frequencies(engine: Engine) -> pd.DataFrame:
    cell_counts = pd.read_sql(
        "SELECT sample_id AS sample, population, count FROM cell_count",
        engine,
    )

    cell_counts["total_count"] = cell_counts.groupby("sample")["count"].transform("sum")
    cell_counts["percentage"] = (
        cell_counts["count"] / cell_counts["total_count"] * 100
    ).round(2)

    return cell_counts[["sample", "total_count", "population", "count", "percentage"]]
