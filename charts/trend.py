"""Role B: data-centre share of electricity demand over time (chart card C1 in docs/BUILD_PLAN.md)."""
import pandas as pd
import streamlit as st


def build_figure(dc_share: pd.DataFrame, regions: list[str]):
    """Return a Plotly Figure, or None when no region is selected."""
    raise NotImplementedError("Role B: build chart card C1")


def render(dc_share: pd.DataFrame) -> None:
    """dc_share is data/processed/dc_share.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    st.caption("TODO (Role B): share-over-time chart with a region selector.")
