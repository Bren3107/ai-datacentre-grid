"""Role C: Story 3 filters, site-size chart and largest-sites table (chart card C4 in docs/BUILD_PLAN.md)."""
import pandas as pd
import streamlit as st


def filter_sites(sites: pd.DataFrame, countries, owners, min_mw, include_zero) -> pd.DataFrame:
    """Return the rows that match the Story 3 filter row."""
    raise NotImplementedError("Role C: apply the filters")


def build_figure(filtered: pd.DataFrame):
    """Return a Plotly Figure, or None when the filtered table is empty."""
    raise NotImplementedError("Role C: build chart card C4")


def render(sites: pd.DataFrame) -> None:
    """sites is data/processed/sites.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    st.caption("TODO (Role C): filters, site-size chart and largest-sites table.")
