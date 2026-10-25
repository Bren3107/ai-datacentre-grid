"""Role D: the page. Opens on the question, a computed answer, the Scale lens, three stories,
the limits, and a "Trace a number" box. Every sentence is in content.py; every number comes
from facts.py; charts come from charts/ (Roles A, B and C)."""
import html
import json
from pathlib import Path

import pandas as pd
import streamlit as st

import content
import theme
from charts import country, owners, trend
from charts import sites as sites_chart
from facts import build_facts

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"

st.set_page_config(
    page_title="AI data centres and the grid", layout="wide", initial_sidebar_state="collapsed"
)


@st.cache_data
def load_data():
    dc_share = pd.read_csv(PROCESSED / "dc_share.csv")
    sites = pd.read_csv(PROCESSED / "sites.csv")
    return dc_share, sites


@st.cache_data
def load_meta():
    return json.loads((PROCESSED / "meta.json").read_text(encoding="utf-8"))


@st.cache_data
def get_facts(entity: str):
    dc_share, sites = load_data()
    return build_facts(dc_share, sites, entity)


def render_lens(entity_options):
    """The Scale selector: one big number and two sentences that change with the scale."""
    st.subheader(content.SCALE_TITLE)
    scale = st.segmented_control(
        content.SCALE_TITLE,
        content.SCALE_OPTIONS,
        default="World",
        required=True,
        key="scale",
        label_visibility="collapsed",
        help=content.SCALE_HELP,
    )
    if scale is None:  # a cleared control counts as World
        scale = "World"
    entity = content.DEFAULT_ENTITY
    if scale == "Country or region":
        entity = st.selectbox(
            content.ENTITY_PICKER,
            entity_options,
            index=entity_options.index(content.DEFAULT_ENTITY),
            key="lens_entity",
        )
    facts = get_facts(entity)
    lens = content.build_lens(scale, facts, entity)
    big, words = st.columns([1, 2])
    with big:
        st.markdown(
            f'<div style="font-size:3rem;font-weight:600;line-height:1.1;color:{theme.INK}">'
            f'{html.escape(lens["hero"])}</div>'
            f'<div style="color:{theme.MUTED};margin-top:0.25rem">{html.escape(lens["label"])}</div>',
            unsafe_allow_html=True,
        )
    with words:
        st.markdown(lens["data"])
        st.markdown(f"**{lens['reading']}**")
    return facts


def render_trace(facts):
    with st.expander(content.TRACE_TITLE):
        st.markdown(content.TRACE_INTRO)
        rows = [
            {
                "Id": fact.id,
                "Shown as": fact.text,
                "Exact value": str(fact.value),
                "Unit": fact.unit,
                "Source file": fact.source_file,
                "How it is calculated": fact.how,
            }
            for fact in facts.values()
        ]
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def footer_values():
    meta = load_meta()
    return {
        "epoch_retrieved": meta["epoch_data_centers"]["retrieved"],
        "epoch_updated": meta["epoch_data_centers"]["source_updated"],
        "owid_retrieved": meta["owid_data_centers_share"]["retrieved"],
        "owid_updated": meta["owid_data_centers_share"]["source_updated"],
    }


dc_share, sites = load_data()
entity_options = sorted(set(dc_share["entity"]) - set(content.NOT_PICKABLE))
base_facts = get_facts(content.DEFAULT_ENTITY)
text = content.fact_values(base_facts)

# ---- opening screen: the question, a true whole-dataset fact, the persona, the answer ----------
st.title(content.QUESTION)
st.markdown(content.fill(content.SUBLINE, text))
st.markdown(content.PERSONA)
st.subheader(content.ANSWER_TITLE)
st.markdown(content.fill(content.ANSWER, text))
st.markdown(content.STORY_LINKS)

# ---- the Scale lens -----------------------------------------------------------------------------
lens_facts = render_lens(entity_options)

# ---- stories -----------------------------------------------------------------------------------
st.header(content.STORY_1_TITLE, anchor="story-1")
st.markdown(content.fill(content.STORY_1_INTRO, text))
trend.render(dc_share)

st.header(content.STORY_2_TITLE, anchor="story-2")
st.markdown(content.STORY_2_INTRO)
country.render(sites)
owners.render(sites)

st.header(content.STORY_3_TITLE, anchor="story-3")
st.markdown(content.fill(content.STORY_3_INTRO, text))
sites_chart.render(sites)

# ---- limits and the other side -----------------------------------------------------------------
left, right = st.columns(2)
with left:
    st.subheader(content.CANNOT_SHOW_TITLE)
    for bullet in content.CANNOT_SHOW:
        st.markdown(f"- {content.fill(bullet, text)}")
with right:
    st.subheader(content.OTHER_SIDE_TITLE)
    st.markdown(content.fill(content.OTHER_SIDE_PLANNING, text))
    st.markdown(content.fill(content.OTHER_SIDE_SMALL, text))

# ---- footer ------------------------------------------------------------------------------------
st.divider()
st.markdown(content.fill(content.FOOTER, footer_values()))
render_trace(lens_facts)
