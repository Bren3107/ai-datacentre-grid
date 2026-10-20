"""Role A: share of tracked AI data-centre power by country (chart card C3 in docs/BUILD_PLAN.md).

Part-to-whole: one 100% stacked horizontal bar, the top 3 countries by estimated IT power plus
"Other countries (n)". Sites at 0 MW are left out, because they add nothing to a share of power.
Epoch's MW figure is IT power, not facility power (docs/DATA_DICTIONARY.md, question 2).
"""
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import theme

META = Path(__file__).resolve().parents[1] / "data" / "processed" / "meta.json"
TOP_N = 3
LABEL_MIN_PCT = 8  # segments narrower than this are labelled in the legend only
BAR_PX = 24
HEIGHT = 260
MARGIN = dict(l=20, r=20, t=60, b=110)  # bottom room for the axis title and the legend

TITLE = "Where tracked AI data-centre IT power is located"
X_TITLE = "Share of tracked estimated IT power (%)"


def country_shares(sites: pd.DataFrame) -> pd.DataFrame:
    """Top countries by MW plus one "Other countries (n)" row: segment, power_mw, share_pct."""
    powered = sites[sites["power_mw"] > 0]
    by_country = powered.groupby("country")["power_mw"].sum().sort_values(ascending=False, kind="stable")
    top = by_country.iloc[:TOP_N]
    rest = by_country.iloc[TOP_N:]
    rows = list(top.items())
    if len(rest):
        rows.append((f"Other countries ({len(rest)})", rest.sum()))
    out = pd.DataFrame(rows, columns=["segment", "power_mw"])
    out["share_pct"] = out["power_mw"] / by_country.sum() * 100
    return out


def segment_color(segment):
    if segment.startswith("Other countries"):
        return theme.CONTEXT_GREY
    return theme.entity_color(segment)


def _luminance(hex_colour):
    channels = [int(hex_colour[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def label_color(fill):
    """White or ink, whichever has the higher WCAG contrast on the segment's fill."""
    fill_lum = _luminance(fill)
    on_white = 1.05 / (fill_lum + 0.05)
    on_ink = (fill_lum + 0.05) / (_luminance(theme.INK) + 0.05)
    return "#FFFFFF" if on_white >= on_ink else theme.INK


def build_figure(sites: pd.DataFrame):
    """Return a Plotly Figure, or None when there is nothing to draw."""
    if sites.empty or not (sites["power_mw"] > 0).any():
        return None
    shares = country_shares(sites)
    fig = go.Figure()
    for segment, mw, pct in shares.itertuples(index=False):
        fill = segment_color(segment)
        fig.add_trace(
            go.Bar(
                x=[pct],
                y=[""],
                orientation="h",
                name=f"{segment} {pct:.1f}%",  # the legend carries every value, so small segments stay readable
                marker=dict(color=fill, line=dict(color=theme.PAPER, width=2)),  # 2 px surface gap
                text=[f"{pct:.1f}%" if pct >= LABEL_MIN_PCT else ""],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color=label_color(fill), size=13),
                customdata=[[segment, mw]],
                hovertemplate="%{customdata[0]}: %{x:.1f}% (%{customdata[1]:,.0f} MW)<extra></extra>",
            )
        )
    theme.apply_layout(fig, TITLE, X_TITLE, None, height=HEIGHT)
    plot_px = HEIGHT - MARGIN["t"] - MARGIN["b"]
    fig.update_layout(
        barmode="stack",
        bargap=1 - BAR_PX / plot_px,
        barcornerradius=4,
        margin=MARGIN,
        showlegend=True,
        legend=dict(orientation="h", x=0, y=-0.9, yanchor="top", traceorder="normal", font=dict(color=theme.INK)),
        uniformtext=dict(minsize=11, mode="hide"),
    )
    fig.update_xaxes(range=[0, 100], ticksuffix="%", dtick=20, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    return fig


def caption(retrieved: str) -> str:
    return (
        "**What it shows:** how the estimated IT power of tracked AI data centres splits across countries; "
        "the three largest countries are named and the rest are grouped. Sites at 0 MW are left out. "
        "Countries reflect what Epoch tracks (its coverage began in the United States), not the world.  \n"
        "**Unit:** % of the total estimated IT power (MW) of tracked sites above 0 MW. "
        "IT power excludes cooling and other facility overhead.  \n"
        f"**Period:** as of {retrieved}.  \n"
        "**Source:** Epoch AI, AI data centers (CC BY 4.0)."
    )


def _retrieved():
    try:
        return json.loads(META.read_text(encoding="utf-8"))["epoch_data_centers"]["retrieved"]
    except (OSError, KeyError, ValueError):
        return "the download date in data/processed/meta.json"


def render(sites: pd.DataFrame) -> None:
    """sites is data/processed/sites.csv (columns in docs/BUILD_PLAN.md section 4.2)."""
    chart_col, notes_col = st.columns([8, 4])
    fig = build_figure(sites)
    with chart_col:
        if fig is None:
            st.info("No tracked sites with power above 0 MW to show.")
        else:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            with st.expander("Show the numbers"):
                table = country_shares(sites).rename(
                    columns={"segment": "Country", "power_mw": "Estimated IT power (MW)", "share_pct": "Share (%)"}
                )
                st.dataframe(
                    table.round({"Estimated IT power (MW)": 0, "Share (%)": 1}),
                    hide_index=True,
                    width="stretch",
                )
    with notes_col:
        st.markdown(caption(_retrieved()))
