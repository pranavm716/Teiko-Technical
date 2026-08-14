import pandas as pd
from sqlalchemy import insert
from sqlalchemy.orm import Session

from db.engine import SessionLocal, engine
from db.tables import Base, Project, Sample, Subject, CellCount

CELL_COUNT_CSV = "data/cell-count.csv"


def load_projects(df: pd.DataFrame, session: Session) -> None:
    projects_df = df[["project"]].drop_duplicates().rename(columns={"project": "id"})
    records = projects_df.to_dict("records")
    session.execute(insert(Project), records)


def load_subjects(df: pd.DataFrame, session: Session) -> None:
    subjects_df = (
        df[["subject", "project", "condition", "age", "sex", "treatment", "response"]]
        .drop_duplicates()
        .rename(columns={"subject": "id", "project": "project_id"})
    )
    subjects_df = subjects_df.where(pd.notnull(subjects_df), None)

    records = subjects_df.to_dict("records")
    session.execute(insert(Subject), records)


def load_samples(df: pd.DataFrame, session: Session) -> None:
    samples_df = (
        df[["sample", "subject", "sample_type", "time_from_treatment_start"]]
        .drop_duplicates()
        .rename(columns={"sample": "id", "subject": "subject_id"})
    )
    records = samples_df.to_dict("records")
    session.execute(insert(Sample), records)


def load_cell_counts(df: pd.DataFrame, session: Session) -> None:
    populations = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]

    cell_counts_df = df.melt(
        id_vars=["sample"],
        value_vars=populations,
        var_name="population",
        value_name="count",
    ).rename(columns={"sample": "sample_id"})

    records = cell_counts_df.to_dict("records")
    session.execute(insert(CellCount), records)


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    df = pd.read_csv(CELL_COUNT_CSV)

    with SessionLocal() as session:
        load_projects(df, session)
        load_subjects(df, session)
        load_samples(df, session)
        load_cell_counts(df, session)
        session.commit()


if __name__ == "__main__":
    main()
