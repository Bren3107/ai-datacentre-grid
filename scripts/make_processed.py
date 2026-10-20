"""Role A: regenerate data/processed/* from data/raw/*.

Run from the repo root: python scripts/make_processed.py
(`--out DIR` writes somewhere else; tests/test_regeneration.py uses it.)

Output schemas are in docs/BUILD_PLAN.md section 4.2; columns and units are in docs/DATA_DICTIONARY.md.
Every CSV is written with index=False and lineterminator="\\n", and the script reads only data/raw/
and the constants below, so a second run writes the same bytes.

Outputs
  dc_share.csv           entity, code, year, share_pct           one row per OWID raw row
  sites.csv              site, owner, owner_confidence, country, power_mw,
                         h100_equivalents, capex_usd_bn_2025, has_power   one row per Epoch raw row
  capacity_timeline.csv  year_end, power_mw_total, is_forecast, n_sites    one row per year-end
  meta.json              per source: url, licence, retrieved, source_updated, raw file size and SHA-256
"""
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

# All three files were downloaded on 20 Oct 2026 at 02:21 UTC (13:21 in Sydney), per the HTTP Date header.
# Epoch's "current" values are the latest record on or before this date.
RETRIEVED = "2026-10-20"
FIRST_TIMELINE_YEAR, LAST_TIMELINE_YEAR = 2019, 2029

EPOCH_FILE = "epoch_data_centers.csv"
OWID_FILE = "owid_data_centers_share_electricity_demand.csv"
TIMELINE_FILE = "epoch_data_center_timelines.csv"
OWID_VALUE_COLUMN = "total_electricity_consumption__share_of_total_electricity_demand__historical"

EPOCH_LICENCE = "Creative Commons Attribution 4.0 (CC BY 4.0), Epoch AI"
SOURCES = {
    "epoch_data_centers": {
        "file": EPOCH_FILE,
        "url": "https://epoch.ai/data/data_centers/data_centers.csv",
        "licence": EPOCH_LICENCE,
        "retrieved": RETRIEVED,
        "source_updated": "2026-10-19",  # Epoch downloads page, "Updated Oct. 19, 2026"
    },
    "owid_data_centers_share": {
        "file": OWID_FILE,
        "url": "https://ourworldindata.org/grapher/data-centers-share-electricity-demand.csv?v=1&csvType=full&useColumnShortNames=true",
        "licence": (
            "OWID processing CC BY 4.0; IEA inputs (c) OECD/IEA under the IEA Terms of Use for Non-CC Material "
            "(https://www.iea.org/terms); Ember inputs CC BY 4.0"
        ),
        "retrieved": RETRIEVED,
        "source_updated": "2026-06-30",  # OWID chart page "Last updated"; indicator metadata updatedAt is 2026-09-10
    },
    "epoch_data_center_timelines": {
        "file": TIMELINE_FILE,
        "url": "https://epoch.ai/data/data_centers/data_center_timelines.csv",
        "licence": EPOCH_LICENCE,
        "retrieved": RETRIEVED,
        "source_updated": "2026-10-19",
    },
}


def read_raw(name):
    # Only truly empty cells become missing, so text such as "NA" stays text.
    return pd.read_csv(RAW / name, keep_default_na=False, na_values=[""])


def write_csv(df, out_dir, name):
    df.to_csv(out_dir / name, index=False, lineterminator="\n")


def make_dc_share():
    raw = read_raw(OWID_FILE)
    if list(raw.columns) != ["entity", "code", "year", OWID_VALUE_COLUMN]:
        raise ValueError(f"unexpected OWID columns: {list(raw.columns)}")
    # Rename the value column; keep entity labels, codes and row order; add and interpolate nothing.
    out = raw.rename(columns={OWID_VALUE_COLUMN: "share_pct"})
    out["year"] = out["year"].astype(int)
    return out[["entity", "code", "year", "share_pct"]]


def make_sites():
    raw = read_raw(EPOCH_FILE)
    owner = raw["Owner"].fillna("").str.strip()
    # The trailing "#word" is Epoch's confidence signifier: "Google #confident" -> "Google", "confident".
    tag = owner.str.extract(r"#(\w+)$")[0].fillna("")
    name = owner.str.replace(r"\s*#\w+$", "", regex=True).str.strip()
    name = name.where(name != "", "Unattributed")
    power = raw["Current power (MW)"]  # Epoch: latest IT power (not facility power), MW
    out = pd.DataFrame(
        {
            "site": raw["Name"],
            "owner": name,
            "owner_confidence": tag,
            "country": raw["Country"],
            "power_mw": power,
            "h100_equivalents": raw["Current H100 equivalents"],
            "capex_usd_bn_2025": raw["Current total capital cost (2025 USD billions)"],
            "has_power": power > 0,  # 0 MW sites stay in the file
        }
    )
    if out["site"].duplicated().any():
        raise ValueError("site names are not unique")
    return out


def it_power_at(timelines, date):
    """Each site's latest IT power value dated on or before `date` (a step function)."""
    upto = timelines[timelines["Date"] <= pd.Timestamp(date)]
    return upto.groupby("Data center")["IT power (MW)"].last()


def read_timelines():
    t = read_raw(TIMELINE_FILE)
    t["Date"] = pd.to_datetime(t["Date"])
    # A row without an IT power value says nothing about power, so the site keeps its previous value.
    t = t.dropna(subset=["IT power (MW)"])
    return t.sort_values(["Data center", "Date"], kind="stable")


def make_capacity_timeline(timelines):
    """Year-end total of each site's latest IT power. Year-ends after the retrieval date are forecasts.

    IT power, because that is what "Current power (MW)" in sites.csv is (see docs/DATA_DICTIONARY.md).
    """
    rows = []
    for year in range(FIRST_TIMELINE_YEAR, LAST_TIMELINE_YEAR + 1):
        year_end = f"{year}-12-31"
        power = it_power_at(timelines, year_end)
        rows.append(
            {
                "year_end": year_end,
                "power_mw_total": round(float(power.sum()), 6),
                "is_forecast": year_end > RETRIEVED,
                "n_sites": int((power > 0).sum()),
            }
        )
    return pd.DataFrame(rows)


def make_meta(sites, timelines):
    meta = {}
    for key, src in SOURCES.items():
        data = (RAW / src["file"]).read_bytes()
        entry = {k: v for k, v in src.items() if k != "file"}
        entry["raw_file"] = f"data/raw/{src['file']}"
        entry["raw_bytes"] = len(data)
        entry["raw_sha256"] = hashlib.sha256(data).hexdigest()
        meta[key] = entry
    # Card C5's built-in check: the timelines file at the retrieval date should equal the sites total.
    timeline_total = round(float(it_power_at(timelines, RETRIEVED).sum()), 6)
    sites_total = round(float(sites["power_mw"].sum()), 6)
    meta["checks"] = {
        "timeline_it_power_at_retrieval_mw": timeline_total,
        "sites_power_total_mw": sites_total,
        "difference_mw": round(abs(timeline_total - sites_total), 6),
    }
    return meta


def main(out_dir=OUT):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dc_share = make_dc_share()
    sites = make_sites()
    timelines = read_timelines()
    timeline = make_capacity_timeline(timelines)
    write_csv(dc_share, out_dir, "dc_share.csv")
    write_csv(sites, out_dir, "sites.csv")
    write_csv(timeline, out_dir, "capacity_timeline.csv")
    meta = make_meta(sites, timelines)
    # Written as bytes so the newline is "\n" on every platform.
    (out_dir / "meta.json").write_bytes((json.dumps(meta, indent=2) + "\n").encode("utf-8"))
    print(
        f"dc_share.csv {len(dc_share)} rows, sites.csv {len(sites)} rows, "
        f"capacity_timeline.csv {len(timeline)} rows, meta.json; written to {out_dir}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=OUT, help="output folder (default: data/processed)")
    main(parser.parse_args().out)
