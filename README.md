# Teiko-Technical

## Run instructions
Run these commands in sequence:
```make
make setup  # Configures environment, installs dependencies
make pipeline  # Populates database (part 1), generates outputs (parts 2-4)
make dashboard  # Launches dashboard locally
```

## Database schema

### Tables

Four tables: `project` → `subject` → `sample` → `cell_count`. Each has a foreign key dependency on the previous table in the chain.

- **project**: `id`
- **subject**: `id`, `project_id`, `condition`, `age`, `sex`, `treatment`, `response` (nullable, since healthy controls have no response)
- **sample**: `id`, `subject_id`, `sample_type`, `time_from_treatment_start`
- **cell_count**: `sample_id`, `population`, `count` (composite PK on `sample_id` + `population`)

### Design rationale
- Each table represents one entity (project, sample, subject, etc.) instead of flattening everything into one wide row per sample. For example, `subject`'s fields (`condition`, `age`, `treatment`, `response`) live once on `subject` and are not repeated across every one of that subject's samples. This means updating a value only requires touching a single row, and there's no way for two samples from the same subject to disagree on their age or treatment.
- `cell_count` stores one row per sample/population pair, rather than a wide table with a column per cell type. This is the shape Part 2's summary table already needs, so no reshaping is required there. It also means adding a new cell population later is just inserting more rows, not changing the table structure.
- Natural keys (`sample_id`, `subject_id`, etc.) are directly used as primary keys rather than surrogate integer IDs, since the source data already provides unique identifiers.
- Added `CHECK` constraints on `subject.response` and `cell_count.population` fields to catch errors at load time.

### Scaling considerations
- Added indexes on `subject.project_id` and `sample.subject_id` fields since they are foreign keys likely to be used in joins. This helps improve query times as the data grows.
- The long format `cell_count` table handles new cell populations as new rows, not a schema change.
- A relational database like Postgres would be used in production instead of SQLite since it can handle larger write volumes.
- Since the schema is fully relational, most new analytics questions are just new SQL queries against existing tables. Schema changes would only be needed if the shape of the underlying data changed, not for new analysis types.

## Repo structure

### `analysis/`
* `part_2_frequencies.py`
* `part_3_statistical_analysis.py`
* `part_4_data_subset_analysis.py`

I kept each part's analysis logic in its own pure function, which return Pandas dataframes. Since the outputs go to two places (file on disk and displayed on the dashboard), I created light wrappers that call these pure functions. This way, no code is repeated.

### `dashboard/app.py`

Code for running the Streamlit dashboard.

### `data/cell-count.csv`

The input CSV.

### `db/`

* `tables.py`: Contains the SQLAlchemy tables.
* `engine.py`: Contains the setup of the SQLite engine.

### `output/`

Contains various output CSVs and boxplots for parts 2-4.

### `load_data.py`

Code for part 1 - responsible for creating and populating the db.

### `run_analysis.py`

Orchestrator file that runs parts 2-4 in sequence, saving outputs for each part. Called by the Makefile.

## Dashboard link

No persistent public link is provided. GitHub Codespaces time out quickly so a link would likely expire by the time it's opened. To view the dashboard, please follow the run instructions at the top within a fresh Codespace.