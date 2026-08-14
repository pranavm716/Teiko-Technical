import os

import pandas as pd
from sqlalchemy.orm import Session

from db.engine import DB_PATH, SessionLocal, engine
from db.tables import Base

CELL_COUNT_CSV = "data/cell-count.csv"


def load_projects(df: pd.DataFrame, session: Session) -> None:
    pass


def load_subjects(df: pd.DataFrame, session: Session) -> None:
    pass


def load_samples(df: pd.DataFrame, session: Session) -> None:
    pass


def load_cell_counts(df: pd.DataFrame, session: Session) -> None:
    pass


def main() -> None:
    Base.metadata.create_all(engine)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)   
        
    df = pd.read_csv(CELL_COUNT_CSV)

    with SessionLocal() as session:
        load_projects(df, session)
        load_subjects(df, session)
        load_samples(df, session)
        load_cell_counts(df, session)
        session.commit()


if __name__ == "__main__":
    main()
