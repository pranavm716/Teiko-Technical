# Teiko-Technical

## Run instructions
Run these commands in sequence:
```Make
make setup  # Configures environment, installs dependencies
make pipeline  # Populates database (part 1), generates outputs (parts 2-4)
make dashboard  # Launches dashboard locally
```

## Database schema

## Repo structure

### `analysis/`
* `part_2_frequencies.py`
* `part_3_statistical_analysis.py`
* `part_4_data_subset_analysis.py`

I kept the business logic of the analysis of each part in their own pure functions. Since the outputs go to two places (file on disk and displayed on the dashboard), I created light wrappers that call the pure functions. This way, no code is repeated.

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