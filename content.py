"""Role D: every sentence the app shows.

Numbers are {placeholders} filled from facts.py; never type a figure by hand.
Copy rules are in docs/BUILD_PLAN.md section 3.4, with one correction: Epoch's megawatts are
estimated IT power (docs/DATA_DICTIONARY.md, question 2), never "facility power".

This module has no Streamlit or pandas imports, so tests can check every sentence directly.
"""

QUESTION = "Is AI data-centre growth a grid problem, or still a small share of electricity demand?"

SUBLINE = (
    "{n_sites} tracked AI data centres in {n_countries} countries, plus the share of electricity "
    "demand used by data centres in {first_year} and from 2023 to {latest_year}."
)

PERSONA = (
    "Written for Priya, a regional energy planner at a transmission or state energy agency. "
    "Her decision: whether data-centre load deserves priority in grid planning now, or can be "
    "monitored for another planning cycle."
)

ANSWER_TITLE = "Our answer"
ANSWER = (
    "**It depends on the scale.** Across the world, data centres used {world_share_latest} of "
    "electricity demand in {latest_year}, which is still small. In the United States the share was "
    "{us_share_latest}, {us_to_world_ratio} times the world figure, and {n_sites_ge_large} of the "
    "{n_sites_power} tracked AI sites are estimated at {large_site_mw} MW of IT power or more each. "
    "These data cannot show whether any particular grid can carry that load."
)

STORY_LINKS = "Jump to: [Story 1](#story-1) | [Story 2](#story-2) | [Story 3](#story-3)"

# ---- the scale lens ---------------------------------------------------------------------------
SCALE_TITLE = "Scale"
SCALE_OPTIONS = ["World", "Country or region", "Site"]
SCALE_HELP = "The same data gives a different answer at each scale. Pick one."
ENTITY_PICKER = "Country or region"
DEFAULT_ENTITY = "United States"
NOT_PICKABLE = ("World", "World excl. United States and China")

LENS_WORLD = {
    "hero": "{world_share_latest}",
    "label": "of world electricity demand went to data centres in {latest_year}",
    "data": "Data: up from {world_share_first} in {first_year}. The figure covers all data centres, not only AI.",
    "reading": "Our reading: at this scale the load is still small.",
}

LENS_ENTITY = {
    "hero": "{entity_share_latest}",
    "label": "of electricity demand in {entity} went to data centres in {latest_year}",
    "data": (
        "Data: that is {entity_to_world_ratio} times the world share, {change_word} "
        "{entity_share_first} in {first_year}. The figure covers all data centres, not only AI."
    ),
}

# Chosen by the ratio of the entity's share to the world share (see reading_key).
LENS_ENTITY_READING = {
    "matter": "Our reading: at this scale the load is large enough to matter for planning.",
    "above": "Our reading: at this scale the load is above the world average.",
    "below": "Our reading: at this scale the load is below the world average.",
}

LENS_SITE = {
    "hero": "{largest_site_mw} MW",
    "label": "estimated IT power of the largest tracked AI data centre, {largest_site_name}",
    "data": (
        "Data: the median tracked site is {median_site_mw} MW. The ten largest hold {top10_share_mw} "
        "of the {total_mw} MW tracked, and {n_sites_ge_large} sites are at or above {large_site_mw} MW "
        "(a threshold our group chose)."
    ),
    "reading": (
        "Our reading: at this scale single sites are large loads. Whether a local grid can carry "
        "one is outside these data."
    ),
}

# ---- stories ----------------------------------------------------------------------------------
STORY_1_TITLE = "Story 1: Is the load still marginal where I plan?"
STORY_1_INTRO = (
    "Share of each region's electricity demand used by data centres, 2020 and 2023 to {latest_year}. "
    "There is no data for 2021 and 2022."
)
STORY_2_TITLE = "Story 2: Who holds the capacity?"
STORY_2_INTRO = (
    "Where the tracked AI data-centre IT power sits, by country and by owner. Both charts use the "
    "whole dataset and do not change with the Story 3 filters."
)
STORY_3_TITLE = "Story 3: How much sits in a few very large sites?"
STORY_3_INTRO = (
    "Filter the tracked sites by country, owner and size. {n_sites_ge_large} of the {n_sites_power} "
    "sites above 0 MW are at or above {large_site_mw} MW; {large_site_mw} MW is a threshold our group "
    "chose, not a figure from the sources."
)

# ---- limits and the other side ---------------------------------------------------------------
CANNOT_SHOW_TITLE = "What these data cannot show"
CANNOT_SHOW = [
    "Whether any particular grid is under strain. Neither file has grid capacity, reserve margins or local demand.",
    "How much of data-centre electricity is for AI. The share file covers all data centres, general-purpose and AI servers together.",
    "Every AI data centre. Epoch lists the major tracked sites, and its coverage began in the United States, so country shares describe what Epoch tracks, not the world.",
    "A site's full demand on the grid. Epoch's megawatts are estimated IT power, which leaves out cooling and other overhead, so the full demand is higher.",
    "Anything about 2021 and 2022, which are missing from the share file, or what happens after {latest_year}. This page makes no forecast.",
    "Whether {latest_year} is a measurement. It is the latest published value, and the sources do not say whether it is preliminary.",
]

OTHER_SIDE_TITLE = "The other side of the argument"
OTHER_SIDE_PLANNING = (
    "**The case that it is already a planning matter.** United States data centres used "
    "{us_share_latest} of electricity demand in {latest_year}, {us_to_world_ratio} times the world "
    "share. In Epoch's tracked sites, {us_share_of_mw} of the estimated IT power is in the United "
    "States, and four named owners hold {top4_owner_share_mw} of the total. A planner works with one "
    "grid, not a world average."
)
OTHER_SIDE_SMALL = (
    "**The case that it is still small.** Data centres used {world_share_latest} of world "
    "electricity demand in {latest_year}, up from {world_share_first} in {first_year}. The tracked AI "
    "sites add up to an estimated {total_mw} MW of IT power, and these data do not show that any "
    "grid is short of capacity."
)

# ---- trace a number and footer ---------------------------------------------------------------
TRACE_TITLE = "Trace a number"
TRACE_INTRO = (
    "Every number in the sentences above is computed in facts.py from a processed file in "
    "data/processed/, which scripts/make_processed.py builds from the raw files in data/raw/. "
    "Pick a row, open the source file, and check the exact value."
)

FOOTER = (
    "**Sources.** Epoch AI, AI data centers and AI data center timelines (CC BY 4.0), retrieved "
    "{epoch_retrieved}; Epoch last updated them on {epoch_updated}. Our World in Data, share of total "
    "electricity demand used by data centers, built on IEA and Ember data (OWID processing and Ember "
    "inputs CC BY 4.0; IEA inputs under the IEA Terms of Use for Non-CC Material), retrieved "
    "{owid_retrieved}; OWID last updated it on {owid_updated}. Whether a public repository may carry "
    "the IEA-derived file is not settled; see docs/DATA_DICTIONARY.md.  \n"
    "**Last data refresh:** {epoch_retrieved}."
)


# ---- helpers (pure, so tests can call them without Streamlit) -------------------------------
def fill(template: str, values: dict) -> str:
    """Fill {placeholders}; raises KeyError for a placeholder with no value."""
    return template.format_map(values)


def reading_key(ratio: float) -> str:
    """Which entity reading applies: 2 or more, 1 to under 2, or under 1 (BUILD_PLAN 3.2)."""
    if ratio >= 2:
        return "matter"
    if ratio >= 1:
        return "above"
    return "below"


def change_word(first: float, latest: float) -> str:
    """'up from', 'down from' or 'level with', judged on the one-decimal values shown."""
    a, b = float(f"{first:.1f}"), float(f"{latest:.1f}")
    if b > a:
        return "up from"
    if b < a:
        return "down from"
    return "level with"


def fact_values(facts: dict, entity: str = DEFAULT_ENTITY) -> dict:
    """Map fact id -> on-screen text, plus the lens entity and its change word."""
    values = {fact_id: fact.text for fact_id, fact in facts.items()}
    values["entity"] = entity
    values["change_word"] = change_word(
        facts["entity_share_first"].value, facts["entity_share_latest"].value
    )
    return values


def build_lens(scale: str, facts: dict, entity: str = DEFAULT_ENTITY) -> dict:
    """Return {'hero', 'label', 'data', 'reading'} for one scale, every placeholder filled."""
    values = fact_values(facts, entity)
    if scale == "Country or region":
        parts = dict(LENS_ENTITY)
        parts["reading"] = LENS_ENTITY_READING[reading_key(facts["entity_to_world_ratio"].value)]
    elif scale == "Site":
        parts = dict(LENS_SITE)
    else:  # "World", and anything unexpected (a cleared control returns None)
        parts = dict(LENS_WORLD)
    return {key: fill(text, values) for key, text in parts.items()}
