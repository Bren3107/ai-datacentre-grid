"""Role B: chart tests (BUILD_PLAN 5.5). The contract lives in tests/chart_contract.py.

Roles A and C: add your builder to BUILDERS below, or call assert_chart_ok in your own test file.
"""
import copy
import csv
from pathlib import Path

import pandas as pd
import pytest

import theme
from charts import country, trend
from tests.chart_contract import assert_chart_ok, assert_empty_returns_none, chart_problems

ROOT = Path(__file__).resolve().parents[1]
RAW_OWID = ROOT / "data" / "raw" / "owid_data_centers_share_electricity_demand.csv"


@pytest.fixture(scope="module")
def dc_share():
    return pd.read_csv(ROOT / "data" / "processed" / "dc_share.csv")


@pytest.fixture(scope="module")
def sites():
    return pd.read_csv(ROOT / "data" / "processed" / "sites.csv", keep_default_na=False, na_values=[""])


def fake_share(rows):
    return pd.DataFrame(rows, columns=["entity", "year", "share_pct"])


# ---- the contract on every builder -------------------------------------------
def test_c1_trend_meets_the_contract(dc_share):
    assert_chart_ok(trend.build_figure(dc_share, trend.DEFAULT_REGIONS))


def test_c1_trend_meets_the_contract_with_six_regions(dc_share):
    six = ["World", "United States", "China", "Europe (IEA)", "North America (IEA)", "Middle East (IEA)"]
    assert_chart_ok(trend.build_figure(dc_share, six))


def test_c3_country_meets_the_contract(sites):
    assert_chart_ok(country.build_figure(sites))


@pytest.mark.parametrize("regions", [[], None, ["Atlantis"]])
def test_c1_empty_selection_returns_none(dc_share, regions):
    assert_empty_returns_none(trend.build_figure, dc_share, regions)
    assert trend.table(dc_share, regions) is None


def test_c3_empty_returns_none(sites):
    assert_empty_returns_none(country.build_figure, sites.iloc[0:0])


# ---- C1 card details -----------------------------------------------------------
def test_c1_axis_titles_carry_the_unit(dc_share):
    fig = trend.build_figure(dc_share, trend.DEFAULT_REGIONS)
    layout = fig.to_plotly_json()["layout"]
    y_titles = {v["title"]["text"] for k, v in layout.items() if k.startswith("yaxis") and v.get("title")}
    x_titles = {v["title"]["text"] for k, v in layout.items() if k.startswith("xaxis") and v.get("title")}
    assert y_titles == {"Share of electricity demand (%)"}
    assert x_titles == {"Year"}


def test_c1_one_label_per_point_one_decimal(dc_share):
    fig = trend.build_figure(dc_share, trend.DEFAULT_REGIONS)
    for tr in fig.data:
        expected = dc_share[dc_share["entity"] == tr.name].sort_values("year")["share_pct"]
        assert list(tr.text) == [f"{v:.1f}%" for v in expected]
        assert "text" in tr.mode


def test_c1_world_2025_label_traces_to_the_raw_file(dc_share):
    with RAW_OWID.open(encoding="utf-8") as f:
        raw = next(r for r in csv.reader(f) if r[0] == "World" and r[2] == "2025")
    assert raw[3] == "1.5264845"
    world = trend.build_figure(dc_share, ["World"]).data[0]
    assert world.text[list(world.x).index(2025)] == "1.5%"
    assert trend.table(dc_share, ["World"]).loc["World", "2025"] == pytest.approx(float(raw[3]))


def test_c1_ticks_and_shared_y_scale(dc_share):
    fig = trend.build_figure(dc_share, trend.DEFAULT_REGIONS)
    layout = fig.to_plotly_json()["layout"]
    xs = [v for k, v in layout.items() if k.startswith("xaxis")]
    ys = [v for k, v in layout.items() if k.startswith("yaxis")]
    assert all(list(a["tickvals"]) == [2020, 2023, 2024, 2025] for a in xs)
    assert len({tuple(a["range"]) for a in ys}) == 1
    assert max(dc_share["share_pct"]) < ys[0]["range"][1]  # headroom so no label clips


def test_c1_no_data_band_on_every_panel(dc_share):
    fig = trend.build_figure(dc_share, trend.DEFAULT_REGIONS)
    bands = [s for s in fig.layout.shapes if s.x0 == 2020.5 and s.x1 == 2022.5]
    notes = [a for a in fig.layout.annotations if a.text == "No data"]
    assert len(bands) == len(notes) == 4


def test_c1_colours_follow_the_entity():
    rows = [(r, y, 1.0) for r in ("World", "United States", "Japan") for y in (2020, 2023)]
    fig = trend.build_figure(fake_share(rows), ["World", "United States", "Japan"])
    colours = {tr.name: tr.line.color for tr in fig.data}
    assert colours == {"World": theme.BLUE, "United States": theme.VERMILLION, "Japan": theme.INK_2}


def test_c1_at_most_six_panels_no_repeats(dc_share):
    many = list(dc_share["entity"].unique()) + ["World"]
    assert len(trend.build_figure(dc_share, many).data) == trend.MAX_REGIONS


def test_c1_layout_rules(dc_share):
    fig = trend.build_figure(dc_share, trend.DEFAULT_REGIONS)
    rows = 2
    assert (fig.layout.height - 130) / rows <= 420
    assert fig.layout.transition.duration == 0


def test_c1_caption_has_the_four_fields_and_the_gap():
    text = trend.caption("2026-10-20")
    for field in ("What it shows", "Unit", "Period", "Source"):
        assert field in text
    assert "no data for 2021 and 2022" in text
    assert "not only AI" in text and "2026-10-20" in text


# ---- the contract must be able to fail (provenance: "a check that could have failed")
@pytest.fixture
def good(dc_share):
    return trend.build_figure(dc_share, ["World", "China"])


def test_contract_fails_when_a_label_is_removed(good):
    broken = copy.deepcopy(good)
    texts = list(broken.data[0].text)
    texts[-1] = ""
    broken.data[0].text = texts
    assert any("labels" in p for p in chart_problems(broken))


def test_contract_fails_on_a_colour_outside_theme(good):
    broken = copy.deepcopy(good)
    broken.data[0].line.color = "#FF00FF"
    assert any("not in theme.py" in p for p in chart_problems(broken))


def test_contract_fails_when_the_unit_is_missing(good):
    broken = copy.deepcopy(good)
    broken.update_yaxes(title_text="Share")
    assert any("no unit" in p for p in chart_problems(broken))


def test_contract_fails_without_a_title(good):
    broken = copy.deepcopy(good)
    broken.update_layout(title_text="")
    assert "figure has no title" in chart_problems(broken)
