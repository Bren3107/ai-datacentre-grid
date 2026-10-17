"""Role A: share of tracked AI data-centre power by country (chart card C3 in docs/BUILD_PLAN.md)."""
import pandas as pd
import streamlit as st


def build_figure(sites: pd.DataFrame):
    """Return a Plotly Figure, or None when there is nothing to draw."""
    raise NotImplementedError("Role A: build chart card C3")


def render(sites: pd.DataFrame) -> None:
    """sites is data/processed/sites.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    st.caption("TODO (Role A): country share chart.")
