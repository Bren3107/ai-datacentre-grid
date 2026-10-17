"""Role B: data-centre share of electricity demand over time (OWID, from IEA and Ember data)."""
import pandas as pd
import streamlit as st


def render(dc_share: pd.DataFrame) -> None:
    """dc_share is data/processed/dc_share.csv (columns in docs/TEAM_PLAN.md)."""
    st.caption("TODO (Role B): share-over-time chart with a region selector.")
