"""Role B: data centres' share of electricity demand over time (chart card C1 in docs/BUILD_PLAN.md).

Change over time: line with markers as small multiples, one panel per selected region,
2 columns, one shared y-scale. Every point is labelled, so no hovering is needed.
OWID has no values for 2021 and 2022; a grey band marks the gap.
"""
import json
import math
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import theme

META = Path(__file__).resolve().parents[1] / "data" / "processed" / "meta.json"

DEFAULT_REGIONS = ["World", "United States", "China", "Europe (IEA)"]
MAX_REGIONS = 6
YEARS = [2020, 2023, 2024, 2025]
GAP = (2020.5, 2022.5)  # covers 2021 and 2022, where the source has no data
X_RANGE = [2019.5, 2025.5]
COLS = 2
PANEL_PX = 190  # plot height per panel row
EMPTY_MESSAGE = "Pick at least one region to draw the chart."

TITLE = "Data centres' share of electricity demand, 2020 to 2025"
X_TITLE = "Year"
Y_TITLE = "Share of electricity demand (%)"


def picked_regions(dc_share: pd.DataFrame, regions) -> list[str]:
    """Known regions only, in the order picked, no repeats, at most MAX_REGIONS."""
    known = set(dc_share["entity"])
    clean = [r for r in dict.fromkeys(regions or []) if r in known]
    return clean[:MAX_REGIONS]


def label(value: float) -> str:
    """One decimal and a % sign (BUILD_PLAN 3.4 rule 6)."""
    return f"{value:.1f}%"


def y_top(values: pd.Series) -> float:
    """Shared y maximum with headroom so the highest label never clips."""
    return max(1.0, math.ceil(values.max() * 1.3 * 2) / 2)


def build_figure(dc_share: pd.DataFrame, regions: list[str]):
    """Return a Plotly Figure, or None when no region is selected."""
    picked = picked_regions(dc_share, regions)
    if not picked:
        return None

    data = dc_share[dc_share["entity"].isin(picked)]
    top = y_top(data["share_pct"])
    rows = math.ceil(len(picked) / COLS)
    cols = COLS if len(picked) > 1 else 1

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=picked,
        shared_yaxes="all",
        vertical_spacing=0.32 / rows,
        horizontal_spacing=0.08,
    )
    for i, region in enumerate(picked):
        row, col = i // cols + 1, i % cols + 1
        points = data[data["entity"] == region].sort_values("year")
        colour = theme.entity_color(region)
        fig.add_annotation(
            x=sum(GAP) / 2, y=top, yanchor="top", text="No data", showarrow=False,
            font=dict(color=theme.MUTED, size=11), row=row, col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=points["year"],
                y=points["share_pct"],
                name=region,
                mode="lines+markers+text",
                line=dict(color=colour, width=2.5),
                marker=dict(color=colour, size=8),
                text=[label(v) for v in points["share_pct"]],
                textposition="top center",
                textfont=dict(color=theme.INK, size=12),
                hovertemplate=f"{region}, %{{x}}: %{{y:.2f}}%<extra></extra>",
                showlegend=False,
            ),
            row=row,
            col=col,
        )
        # After the trace: Plotly skips shapes on a panel that has no trace yet.
        fig.add_vrect(x0=GAP[0], x1=GAP[1], fillcolor=theme.GRID, opacity=0.7, line_width=0, layer="below", row=row, col=col)

    height = rows * PANEL_PX + 130
    theme.apply_layout(fig, TITLE, None, None, height=height)
    fig.update_layout(margin=dict(l=60, r=20, t=90, b=50))
    fig.update_xaxes(range=X_RANGE, tickvals=YEARS, ticktext=[str(y) for y in YEARS], fixedrange=True, showgrid=False)
    fig.update_yaxes(range=[0, top], fixedrange=True)
    for c in range(1, cols + 1):  # x title on the bottom panels only
        fig.update_xaxes(title_text=X_TITLE, title_font=dict(size=13), row=rows, col=c)
    if len(picked) % cols and rows > 1:  # odd count: the last panel sits alone, title the one above too
        fig.update_xaxes(title_text=X_TITLE, title_font=dict(size=13), row=rows - 1, col=cols)
    for r in range(1, rows + 1):  # y title on the left panels only
        fig.update_yaxes(title_text=Y_TITLE, title_font=dict(size=13), row=r, col=1)
    for annotation in fig.layout.annotations:
        if annotation.text in picked:
            annotation.font = dict(color=theme.INK, size=14)
    return fig


def table(dc_share: pd.DataFrame, regions: list[str]):
    """'Show the numbers' twin: one row per region, one column per year, unrounded % values."""
    picked = picked_regions(dc_share, regions)
    if not picked:
        return None
    out = (
        dc_share[dc_share["entity"].isin(picked)]
        .pivot(index="entity", columns="year", values="share_pct")
        .reindex(picked)
    )
    out.columns = [str(c) for c in out.columns]
    out.index.name = "Region"
    return out


def caption(retrieved: str) -> str:
    return (
        "**What it shows:** data centres' share of each region's total electricity demand; "
        "one panel per region, all on the same scale. Covers all data centres, not only AI.  \n"
        "**Unit:** % of that region's electricity demand in that year.  \n"
        "**Period:** 2020 and 2023 to 2025; no data for 2021 and 2022 (grey band).  \n"
        "**Source:** IEA 'Energy and AI' and Ember, via Our World in Data, "
        f"retrieved {retrieved}."
    )


def _retrieved():
    try:
        return json.loads(META.read_text(encoding="utf-8"))["owid_data_centers_share"]["retrieved"]
    except (OSError, KeyError, ValueError):
        return "on the date in data/processed/meta.json"


def region_options(dc_share: pd.DataFrame) -> list[str]:
    entities = list(dict.fromkeys(dc_share["entity"]))
    return [r for r in DEFAULT_REGIONS if r in entities] + sorted(r for r in entities if r not in DEFAULT_REGIONS)


def render(dc_share: pd.DataFrame) -> None:
    """dc_share is data/processed/dc_share.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    options = region_options(dc_share)
    regions = st.multiselect(
        "Regions",
        options,
        default=[r for r in DEFAULT_REGIONS if r in options],
        max_selections=MAX_REGIONS,
        key="trend_regions",
        help="Up to 6 regions. Each gets its own panel on the same scale.",
    )
    chart_col, notes_col = st.columns([8, 4])
    fig = build_figure(dc_share, regions)
    with chart_col:
        if fig is None:
            st.info(EMPTY_MESSAGE)
        else:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            with st.expander("Show the numbers"):
                st.caption("Share of electricity demand (%), as in the source file (unrounded).")
                st.dataframe(table(dc_share, regions), width="stretch")
    with notes_col:
        st.markdown(caption(_retrieved()))
