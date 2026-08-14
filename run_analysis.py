import os

from analysis.part_2_frequencies import compute_frequencies
from db.engine import engine

OUTPUT_DIR = "output"


def run_part_2_frequencies() -> None:
    frequencies = compute_frequencies(engine)
    frequencies.to_csv(f"{OUTPUT_DIR}/part_2_frequencies.csv", index=False)
    print("run_analysis.py: part 2 frequencies written")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    run_part_2_frequencies()


if __name__ == "__main__":
    main()
