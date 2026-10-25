"""Role D: the wording rules from docs/BUILD_PLAN.md section 3.4, enforced on content.py."""
import re
from pathlib import Path

import pandas as pd

import content
from facts import build_facts

ROOT = Path(__file__).resolve().parents[1]
BANNED = ["caus", "crisis", "will", "ai uses", "facility power", "consumption"]


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _all_copy(skip=()):
    """Every sentence in content.py (names in ALL CAPS), minus the named constants in `skip`."""
    out = []
    for name, value in vars(content).items():
        if name.isupper() and name not in skip:
            out.extend(_strings(value))
    return out


def test_no_banned_wording():
    for sentence in _all_copy():
        for stem in BANNED:
            assert stem not in sentence.lower(), f"{stem!r} found in: {sentence}"


def test_strain_only_in_the_cannot_show_list():
    for sentence in _all_copy(skip=("CANNOT_SHOW",)):
        assert "strain" not in sentence.lower(), sentence


def test_no_hand_typed_figures():
    """Digits are allowed only for the years the data covers, '0 MW', and story numbers."""
    allowed = [r"CC BY 4\.0", r"\b20(?:20|21|22|23)\b", r"\b0 MW\b", r"Story \d", r"#story-\d"]
    for sentence in _all_copy():
        text = re.sub(r"\{[^}]*\}", "", sentence)  # placeholder names such as {top10_share_mw}
        for pattern in allowed:
            text = re.sub(pattern, "", text)
        assert not re.search(r"\d", text), f"hand-typed figure in: {sentence}"


def test_cannot_show_has_at_least_four_bullets():
    assert len(content.CANNOT_SHOW) >= 4


def test_every_placeholder_fills_for_every_scale_and_region():
    dc_share = pd.read_csv(ROOT / "data/processed/dc_share.csv")
    sites = pd.read_csv(ROOT / "data/processed/sites.csv")
    entities = sorted(set(dc_share["entity"]) - set(content.NOT_PICKABLE))
    assert len(entities) == 8
    for entity in entities:
        facts = build_facts(dc_share, sites, entity)
        values = content.fact_values(facts, entity)
        for sentence in _all_copy(skip=("FOOTER",)):
            assert "{" not in content.fill(sentence, values)
        for scale in content.SCALE_OPTIONS:
            lens = content.build_lens(scale, facts, entity)
            assert set(lens) == {"hero", "label", "data", "reading"}
            assert not any("{" in part or "}" in part for part in lens.values())
