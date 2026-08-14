import streamlit as st

from analysis.part_2_frequencies import compute_frequencies
from db.engine import engine
from load_data import POPULATIONS


def render_part_2_frequencies() -> None:
    st.header("Part 2: Population Frequencies by Sample")

    @st.cache_data
    def load_frequencies():
        return compute_frequencies(engine)

    frequencies = load_frequencies()

    col1, col2 = st.columns([2, 1])
    with col1:
        sample_search = st.text_input(
            "Filter by sample ID", placeholder="e.g. sample00042"
        )
    with col2:
        populations = st.multiselect(
            "Filter by population",
            options=POPULATIONS,
            default=None,
        )

    filtered = frequencies
    if sample_search:
        filtered = filtered[filtered["sample"].str.contains(sample_search, case=False)]
    if populations:
        filtered = filtered[filtered["population"].isin(populations)]

    st.caption(f"Showing {len(filtered):,} of {len(frequencies):,} rows")
    st.dataframe(filtered, width="stretch", hide_index=True)


def main() -> None:
    st.set_page_config(page_title="Teiko - Cell Population Analysis", layout="wide")
    st.title("Immune Cell Population Analysis")

    render_part_2_frequencies()


if __name__ == "__main__":
    main()
