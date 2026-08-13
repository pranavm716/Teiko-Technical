from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "project"
    id: Mapped[str] = mapped_column(primary_key=True)


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    condition: Mapped[str]
    age: Mapped[int]
    sex: Mapped[str]
    treatment: Mapped[str]
    response: Mapped[str]


class Sample(Base):
    __tablename__ = "sample"

    id: Mapped[str] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    sample_type: Mapped[str]
    time_from_treatment_start: Mapped[int]


class CellCount(Base):
    __tablename__ = "cell_count"

    sample_id: Mapped[str] = mapped_column(ForeignKey("sample.id"), primary_key=True)
    population: Mapped[str] = mapped_column(primary_key=True)
    count: Mapped[int]
