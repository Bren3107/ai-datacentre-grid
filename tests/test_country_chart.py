"""Role A: chart card C3 (share of tracked AI data-centre IT power by country)."""
from pathlib import Path

import pandas as pd
import pytest

import theme
from charts import country

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def sites():
    return pd.read_csv(ROOT / "data" / "processed" / "sites.csv", keep_default_na=False, na_values=[""])


def fake_sites(rows):
    return pd.DataFrame(rows, columns=["site", "country", "power_mw"]).assign(has_power=lambda d: d.power_mw > 0)


def test_shares_are_top_three_plus_other(sites):
    shares = country.country_shares(sites)
    assert len(shares) == 4
    assert shares["segment"].iloc[-1].startswith("Other countries (")
    assert shares["share_pct"].iloc[:3].is_monotonic_decreasing


def test_shares_match_an_independent_recomputation(sites):
    # Different expression from the module: pivot on the raw rows, then share of the grand total.
    powered = sites.query("power_mw > 0")
    by_country = powered.pivot_table(index="country", values="power_mw", aggfunc="sum")["power_mw"]
    expected = (by_country / by_country.sum() * 100).sort_values(ascending=False)
    shares = country.country_shares(sites).set_index("segment")["share_pct"]
    for name in expected.index[:3]:
        assert shares[name] == pytest.approx(expected[name])
    assert shares.iloc[-1] == pytest.approx(expected.iloc[3:].sum())
    assert shares.index[-1] == f"Other countries ({len(expected) - 3})"


def test_segments_sum_to_100(sites):
    fig = country.build_figure(sites)
    assert sum(sum(trace.x) for trace in fig.data) == pytest.approx(100)


def test_legend_text_contains_every_value(sites):
    fig = country.build_figure(sites)
    shares = country.country_shares(sites)
    names = [trace.name for trace in fig.data]
    for segment, pct in zip(shares["segment"], shares["share_pct"]):
        assert f"{segment} {pct:.1f}%" in names


def test_zero_mw_sites_are_excluded():
    rows = [("a", "United States", 300.0), ("b", "China", 100.0), ("c", "Norway", 0.0)]
    shares = country.country_shares(fake_sites(rows))
    assert shares["segment"].tolist() == ["United States", "China"]
    assert shares["share_pct"].tolist() == [75.0, 25.0]


def test_no_other_segment_when_three_countries_or_fewer():
    rows = [("a", "United States", 50.0), ("b", "China", 30.0), ("c", "Malaysia", 20.0)]
    assert "Other" not in " ".join(country.country_shares(fake_sites(rows))["segment"])


def test_colours_follow_the_entity():
    rows = [("a", "United States", 50.0), ("b", "China", 30.0), ("c", "Malaysia", 15.0), ("d", "Norway", 5.0), ("e", "Iceland", 1.0)]
    fig = country.build_figure(fake_sites(rows))
    colours = {trace.name.rsplit(" ", 1)[0]: trace.marker.color for trace in fig.data}
    assert colours["United States"] == theme.VERMILLION
    assert colours["China"] == theme.GREEN
    assert colours["Malaysia"] == theme.INK_2
    assert colours["Other countries (2)"] == theme.CONTEXT_GREY


def test_only_segments_of_8_percent_or_more_are_labelled_inside():
    rows = [("a", "United States", 90.0), ("b", "China", 7.0), ("c", "Malaysia", 3.0)]
    fig = country.build_figure(fake_sites(rows))
    labels = {trace.name: trace.text[0] for trace in fig.data}
    assert labels["United States 90.0%"] == "90.0%"
    assert labels["China 7.0%"] == ""
    assert labels["Malaysia 3.0%"] == ""


def test_title_and_axis_title_name_it_power_and_unit(sites):
    fig = country.build_figure(sites)
    assert "IT power" in fig.layout.title.text
    assert fig.layout.xaxis.title.text == "Share of tracked estimated IT power (%)"
    assert "facility" not in (fig.layout.title.text + fig.layout.xaxis.title.text).lower()
    assert fig.layout.yaxis.visible is False


def test_layout_rules(sites):
    fig = country.build_figure(sites)
    assert fig.layout.barmode == "stack"
    assert fig.layout.height <= 420
    assert fig.layout.transition.duration == 0
    assert list(fig.layout.xaxis.range) == [0, 100]


def test_empty_input_returns_none():
    assert country.build_figure(fake_sites([])) is None


def test_all_zero_input_returns_none():
    assert country.build_figure(fake_sites([("a", "United States", 0.0)])) is None


def test_caption_has_the_four_fields_and_the_coverage_warning():
    caption = country.caption("2026-10-20")
    for field in ("What it shows", "Unit", "Period", "Source"):
        assert field in caption
    assert "Countries reflect what Epoch tracks (its coverage began in the United States), not the world." in caption
    assert "2026-10-20" in caption
