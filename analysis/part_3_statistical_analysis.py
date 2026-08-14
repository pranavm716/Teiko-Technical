import pandas as pd
from sqlalchemy.engine import Engine

from analysis.part_2_frequencies import compute_frequencies


def get_group_frequencies(engine: Engine) -> pd.DataFrame:
    freq_df = compute_frequencies(engine)

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

    merged = freq_df.merge(metadata, on="sample")

    return merged[
        (merged["condition"] == "melanoma")
        & (merged["treatment"] == "miraclib")
        & (merged["sample_type"] == "PBMC")
        & (merged["response"].notna())
    ]
