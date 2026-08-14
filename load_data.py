import pandas as pd
from sqlalchemy import insert
from sqlalchemy.orm import Session

from db.engine import SessionLocal, engine
from db.tables import Base, Project

CELL_COUNT_CSV = "data/cell-count.csv"


def load_projects(df: pd.DataFrame, session: Session) -> None:
    projects_df = df[["project"]].drop_duplicates().rename(columns={"project": "id"})
    records = projects_df.to_dict("records")
    session.execute(insert(Project), records)


def load_subjects(df: pd.DataFrame, session: Session) -> None:
    pass


def load_samples(df: pd.DataFrame, session: Session) -> None:
    pass


def load_cell_counts(df: pd.DataFrame, session: Session) -> None:
    pass


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
