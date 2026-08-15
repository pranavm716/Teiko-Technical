# analysis/part_4_subset_analysis.py
import pandas as pd
from sqlalchemy.engine import Engine


def get_baseline_samples(engine: Engine) -> pd.DataFrame:
    query = """
        SELECT
            sample.id AS sample_id,
            sample.time_from_treatment_start,
            subject.id AS subject_id,
            subject.project_id,
            subject.response,
            subject.sex
        FROM sample
        JOIN subject ON sample.subject_id = subject.id
        WHERE subject.condition = 'melanoma'
          AND subject.treatment = 'miraclib'
          AND sample.sample_type = 'PBMC'
          AND sample.time_from_treatment_start = 0
    """
    return pd.read_sql(query, engine)
