import pandas as pd
import streamlit as st

from analysis.part_2_frequencies import compute_frequencies
from analysis.part_3_statistical_analysis import (
    compute_stats,
    generate_boxplots,
    get_group_frequencies,
)
from db.engine import engine
from load_data import POPULATIONS


@st.cache_data
def load_all_frequencies() -> pd.DataFrame:
    return compute_frequencies(engine)


@st.cache_data
def load_group_frequencies(all_frequencies: pd.DataFrame) -> pd.DataFrame:
    return get_group_frequencies(all_frequencies, engine)


def render_part_2_frequencies(all_frequencies: pd.DataFrame) -> None:
    st.header("Part 2: Population Frequencies by Sample")

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

    filtered = all_frequencies
    if sample_search:
        filtered = filtered[filtered["sample"].str.contains(sample_search, case=False)]
    if populations:
        filtered = filtered[filtered["population"].isin(populations)]

    st.caption(f"Showing {len(filtered):,} of {len(all_frequencies):,} rows")
    st.dataframe(filtered, width="stretch", hide_index=True)


def render_part_3_statistical_analysis(group_frequencies: pd.DataFrame) -> None:
    st.header("Part 3: Responder vs Non-Responder Statistical Analysis")
    st.caption(
        "Melanoma patients on miraclib, PBMC samples only. "
        "Ran a Mann-Whitney U test per population. Since we have 5 comparisons, "
        "we also need to apply a Bonferroni correction."
    )

    stats_summary = compute_stats(group_frequencies)
    st.dataframe(stats_summary, width="stretch", hide_index=True)

    st.subheader("Relative Frequency by Response")
    boxplots = generate_boxplots(group_frequencies)

    cols = st.columns(2)
    for i, population in enumerate(POPULATIONS):
        with cols[i % 2]:
            st.pyplot(boxplots[population])

    st.subheader("Summary")
    st.markdown(
        """
        None of the 5 cell populations showed a statistically significant difference
        between responders and non-responders, after correcting for running 5 tests.

        The p_value for cd4_t_cell came close (0.0134), but became too high once the Bonferroni correction was applied (0.067).

        As a result, none of these 5 populations reliably predicts whether a patient responds to miraclib.
        """
    )


def main() -> None:
    st.set_page_config(page_title="Teiko - Cell Population Analysis", layout="wide")
    st.title("Immune Cell Population Analysis")

    all_frequencies = load_all_frequencies()
    group_frequencies = load_group_frequencies(all_frequencies)

    render_part_2_frequencies(all_frequencies)
    render_part_3_statistical_analysis(group_frequencies)


if __name__ == "__main__":
    main()
