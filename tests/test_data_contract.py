"""Role A: the data contract in docs/BUILD_PLAN.md section 4.3.

Checks the committed files in data/processed/ against data/raw/. Where a test recomputes a value
from a raw file, it uses the csv module or a different pandas expression from the one in
scripts/make_processed.py, so a bug in the script cannot also hide in the test.
"""
import csv
import hashlib
import json
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

RAW_FILES = {
    "epoch_data_centers": "epoch_data_centers.csv",
    "owid_data_centers_share": "owid_data_centers_share_electricity_demand.csv",
    "epoch_data_center_timelines": "epoch_data_center_timelines.csv",
}
PROCESSED_FILES = ["dc_share.csv", "sites.csv", "capacity_timeline.csv", "meta.json"]


def raw_rows(name):
    with open(RAW / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def dc_share():
    return pd.read_csv(PROCESSED / "dc_share.csv")


@pytest.fixture(scope="module")
def sites():
    return pd.read_csv(PROCESSED / "sites.csv", keep_default_na=False, na_values=[""])


@pytest.fixture(scope="module")
def timeline():
    return pd.read_csv(PROCESSED / "capacity_timeline.csv")


@pytest.fixture(scope="module")
def meta():
    return json.loads((PROCESSED / "meta.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", list(RAW_FILES.values()))
def test_raw_file_exists(name):
    assert (RAW / name).is_file()


@pytest.mark.parametrize("name", PROCESSED_FILES)
def test_processed_file_exists(name):
    assert (PROCESSED / name).is_file()


# dc_share.csv


def test_dc_share_columns_and_dtypes(dc_share):
    assert list(dc_share.columns) == ["entity", "code", "year", "share_pct"]
    assert dc_share["year"].dtype == "int64"
    assert dc_share["share_pct"].dtype == "float64"


def test_dc_share_is_a_percentage(dc_share):
    assert dc_share["share_pct"].between(0, 100).all()


def test_dc_share_years_are_the_published_set(dc_share):
    assert set(dc_share["year"]) == {2020, 2023, 2024, 2025}


def test_dc_share_has_one_row_per_raw_row(dc_share):
    assert len(dc_share) == len(raw_rows(RAW_FILES["owid_data_centers_share"]))


def test_dc_share_key_is_unique(dc_share):
    assert not dc_share.duplicated(["entity", "year"]).any()


def test_dc_share_values_equal_raw_values(dc_share):
    rows = raw_rows(RAW_FILES["owid_data_centers_share"])
    value_col = [c for c in rows[0] if c not in ("entity", "code", "year")][0]
    raw = {(r["entity"], int(r["year"])): float(r[value_col]) for r in rows}
    got = {(e, int(y)): v for e, y, v in dc_share[["entity", "year", "share_pct"]].itertuples(index=False)}
    assert got == raw


# sites.csv

SITES_COLUMNS = [
    "site",
    "owner",
    "owner_confidence",
    "country",
    "power_mw",
    "h100_equivalents",
    "capex_usd_bn_2025",
    "has_power",
]


def test_sites_columns_and_dtypes(sites):
    assert list(sites.columns) == SITES_COLUMNS
    assert sites["power_mw"].dtype == "float64"
    assert sites["h100_equivalents"].dtype == "float64"
    assert sites["capex_usd_bn_2025"].dtype == "float64"
    assert sites["has_power"].dtype == "bool"


def test_sites_has_one_row_per_raw_row(sites):
    assert len(sites) == len(raw_rows(RAW_FILES["epoch_data_centers"]))


def test_site_is_unique(sites):
    assert sites["site"].is_unique


def test_power_is_not_negative(sites):
    assert (sites["power_mw"] >= 0).all()


def test_no_tag_left_in_owner(sites):
    assert not sites["owner"].str.contains("#").any()
    assert not sites["owner"].str.strip().ne(sites["owner"]).any()


def test_blank_owner_becomes_unattributed(sites):
    raw_blank = sum(1 for r in raw_rows(RAW_FILES["epoch_data_centers"]) if not r["Owner"].strip())
    assert raw_blank > 0
    assert (sites["owner"] == "Unattributed").sum() == raw_blank


def test_owner_and_tag_rebuild_the_raw_owner(sites):
    # Independent of the script's regex: rebuild "Owner #tag" from the two output columns.
    raw = [r["Owner"].strip() for r in raw_rows(RAW_FILES["epoch_data_centers"])]
    for (owner, tag), original in zip(sites[["owner", "owner_confidence"]].itertuples(index=False), raw):
        if not original:
            assert owner == "Unattributed" and pd.isna(tag)
        elif pd.isna(tag):
            assert owner == original
        else:
            assert f"{owner} #{tag}" == re.sub(r"\s+#", " #", original)


def test_confidence_tags_are_the_documented_three(sites):
    assert set(sites["owner_confidence"].dropna()) <= {"confident", "likely", "speculative"}


def test_has_power_matches_power(sites):
    assert (sites["has_power"] == (sites["power_mw"] > 0)).all()


def test_zero_mw_sites_are_kept(sites):
    raw_zero = sum(1 for r in raw_rows(RAW_FILES["epoch_data_centers"]) if float(r["Current power (MW)"]) == 0)
    assert raw_zero > 0
    assert (~sites["has_power"]).sum() == raw_zero


def test_compute_and_cost_are_not_negative(sites):
    assert (sites["h100_equivalents"] >= 0).all()
    assert (sites["capex_usd_bn_2025"] >= 0).all()


def test_total_power_equals_raw_total(sites):
    raw_total = sum(float(r["Current power (MW)"]) for r in raw_rows(RAW_FILES["epoch_data_centers"]))
    assert sites["power_mw"].sum() == pytest.approx(raw_total, abs=1e-6)


# capacity_timeline.csv


def test_timeline_columns_and_dtypes(timeline):
    assert list(timeline.columns) == ["year_end", "power_mw_total", "is_forecast", "n_sites"]
    assert timeline["power_mw_total"].dtype == "float64"
    assert timeline["is_forecast"].dtype == "bool"
    assert timeline["n_sites"].dtype == "int64"


def test_timeline_has_one_row_per_year_end_2019_to_2029(timeline):
    assert timeline["year_end"].tolist() == [f"{y}-12-31" for y in range(2019, 2030)]


def test_forecast_flag_follows_the_retrieval_date(timeline, meta):
    retrieved = meta["epoch_data_center_timelines"]["retrieved"]
    assert (timeline["is_forecast"] == (timeline["year_end"] > retrieved)).all()


def test_timeline_counts_and_totals_are_in_range(timeline, sites):
    assert (timeline["power_mw_total"] >= 0).all()
    assert timeline["n_sites"].between(0, len(sites)).all()


def test_timeline_never_falls(timeline):
    # Epoch records capacity, which only grows in this file; a fall would mean a broken step function.
    assert timeline["power_mw_total"].is_monotonic_increasing


def test_timeline_at_retrieval_matches_sites_total(meta, sites):
    # Built-in check from chart card C5: the timelines file, summed at the retrieval date, must land on
    # the data_centers.csv total. Recomputed here from the raw file with the csv module.
    retrieved = meta["epoch_data_center_timelines"]["retrieved"]
    latest = {}
    for r in raw_rows(RAW_FILES["epoch_data_center_timelines"]):
        if r["Date"] <= retrieved and r["IT power (MW)"] != "":
            if r["Data center"] not in latest or r["Date"] >= latest[r["Data center"]][0]:
                latest[r["Data center"]] = (r["Date"], float(r["IT power (MW)"]))
    assert sum(v for _, v in latest.values()) == pytest.approx(sites["power_mw"].sum(), abs=1e-6)
    assert meta["checks"]["difference_mw"] == pytest.approx(0, abs=1e-6)


# meta.json


@pytest.mark.parametrize("key", list(RAW_FILES))
def test_meta_has_the_four_fields(meta, key):
    for field in ("url", "licence", "retrieved", "source_updated"):
        assert meta[key][field], f"{key}.{field} is empty"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta[key]["retrieved"])
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta[key]["source_updated"])


@pytest.mark.parametrize("key,name", list(RAW_FILES.items()))
def test_raw_file_is_unchanged_since_download(meta, key, name):
    data = (RAW / name).read_bytes()
    assert len(data) == meta[key]["raw_bytes"]
    assert hashlib.sha256(data).hexdigest() == meta[key]["raw_sha256"]
