"""Role A: AI data-centre capacity by country (Epoch AI data centres)."""
import pandas as pd
import streamlit as st


def render(sites: pd.DataFrame) -> None:
    """sites is data/processed/sites.csv (columns in docs/TEAM_PLAN.md)."""
    st.caption("TODO (Role A): capacity (MW) by country.")
