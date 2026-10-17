"""Role D: opening-screen headline facts, computed from the processed data."""
import pandas as pd
import streamlit as st


def render(dc_share: pd.DataFrame, sites: pd.DataFrame) -> None:
    """dc_share and sites are the processed files (columns in docs/TEAM_PLAN.md)."""
    st.caption("TODO (Role D): stat tiles and one comparison chart.")
