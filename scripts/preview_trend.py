"""Role B: run C1 on its own until it is wired into app.py.

    streamlit run scripts/preview_trend.py
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from charts import trend  # noqa: E402
from content import QUESTION  # noqa: E402

st.set_page_config(page_title="C1 preview", layout="wide")
st.title(QUESTION)
st.subheader("Story 1: is the share rising, and where?")
trend.render(pd.read_csv(ROOT / "data" / "processed" / "dc_share.csv"))
