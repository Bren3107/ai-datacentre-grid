"""Role C: tracked AI data-centre power by owner (chart card C2 in docs/BUILD_PLAN.md)."""
import pandas as pd
import streamlit as st


def build_figure(sites: pd.DataFrame):
    """Return a Plotly Figure, or None when there is nothing to draw."""
    raise NotImplementedError("Role C: build chart card C2")


def render(sites: pd.DataFrame) -> None:
    """sites is data/processed/sites.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    st.caption("TODO (Role C): owner ranking chart.")
