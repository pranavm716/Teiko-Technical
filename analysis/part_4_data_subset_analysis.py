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


def summarize_baseline_breakdown(
    baseline_samples: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    by_project = (
        baseline_samples.groupby("project_id").size().reset_index(name="sample_count")
    )

    by_response = (
        baseline_samples.groupby("response")["subject_id"]
        .nunique()
        .reset_index(name="subject_count")
    )

    by_sex = (
        baseline_samples.groupby("sex")["subject_id"]
        .nunique()
        .reset_index(name="subject_count")
    )

    return {
        "by_project": by_project,
        "by_response": by_response,
        "by_sex": by_sex,
    }


def compute_average_b_cells_melanoma_male_responders(engine: Engine) -> float:
    query = """
        SELECT cell_count.count
        FROM cell_count
        JOIN sample ON cell_count.sample_id = sample.id
        JOIN subject ON sample.subject_id = subject.id
        WHERE subject.condition = 'melanoma'
          AND subject.sex = 'M'
          AND subject.response = 'yes'
          AND sample.time_from_treatment_start = 0
          AND cell_count.population = 'b_cell'
    """
    b_cell_counts = pd.read_sql(query, engine)
    return round(b_cell_counts["count"].mean(), 2)
