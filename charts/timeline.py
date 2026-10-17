"""Role B (SHOULD): tracked capacity to date and forecast (chart card C5 in docs/BUILD_PLAN.md)."""
import pandas as pd
import streamlit as st


def build_figure(capacity: pd.DataFrame):
    """Return a Plotly Figure, or None when there is nothing to draw."""
    raise NotImplementedError("Role B: build chart card C5")


def render(capacity: pd.DataFrame) -> None:
    """capacity is data/processed/capacity_timeline.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    st.caption("TODO (Role B): capacity timeline.")
