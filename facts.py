"""Role D: the fact registry.

Every number shown inside a sentence is built here from the processed data, so each one
can be traced to a file and a computation. The list of ids is in docs/BUILD_PLAN.md section 3.5.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

import pandas as pd

LARGE_SITE_MW = 200  # group choice; the app shows it on screen as such

DC_SHARE_FILE = "data/processed/dc_share.csv"
SITES_FILE = "data/processed/sites.csv"
WORLD = "World"
US = "United States"


@dataclass(frozen=True)
class Fact:
    id: str
    value: Any
    text: str  # how it appears on screen, for example "1.5%"
    unit: str
    source_file: str  # for example "data/processed/dc_share.csv"
    how: str  # one line describing the computation


def _pct(x: float) -> str:
    return f"{x:.1f}%"


def _mw(x: float) -> str:
    """Whole megawatts with a thousands separator, rounding .5 up (152.5 -> 153, not 152)."""
    return f"{int(Decimal(str(x)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}"


def _share(dc_share: pd.DataFrame, entity: str, year: int) -> float:
    rows = dc_share[(dc_share["entity"] == entity) & (dc_share["year"] == year)]
    if rows.empty:
        raise ValueError(f"No share value for {entity!r} in {year}")
    return float(rows["share_pct"].iloc[0])


def build_facts(
    dc_share: pd.DataFrame, sites: pd.DataFrame, entity: str = US
) -> dict[str, Fact]:
    """Return every fact keyed by id.

    `entity` is the region picked in the "Country or region" lens; the three
    entity_* facts use it. Everything else is independent of it.
    """
    facts: dict[str, Fact] = {}

    def add(id_: str, value: Any, text: str, unit: str, source: str, how: str) -> None:
        facts[id_] = Fact(id_, value, text, unit, source, how)

    # --- share of electricity demand (dc_share.csv) ---------------------------------
    latest_year = int(dc_share["year"].max())
    first_year = int(dc_share["year"].min())
    add("latest_year", latest_year, str(latest_year), "year", DC_SHARE_FILE,
        "Largest value in the year column")
    add("first_year", first_year, str(first_year), "year", DC_SHARE_FILE,
        "Smallest value in the year column")

    world_latest = _share(dc_share, WORLD, latest_year)
    world_first = _share(dc_share, WORLD, first_year)
    us_latest = _share(dc_share, US, latest_year)
    add("world_share_latest", world_latest, _pct(world_latest), "% of electricity demand",
        DC_SHARE_FILE, f"share_pct where entity = World and year = {latest_year}")
    add("world_share_first", world_first, _pct(world_first), "% of electricity demand",
        DC_SHARE_FILE, f"share_pct where entity = World and year = {first_year}")
    add("us_share_latest", us_latest, _pct(us_latest), "% of electricity demand",
        DC_SHARE_FILE, f"share_pct where entity = United States and year = {latest_year}")
    add("us_to_world_ratio", us_latest / world_latest, f"{us_latest / world_latest:.1f}",
        "ratio", DC_SHARE_FILE, "United States share divided by World share, latest year")

    ent_latest = _share(dc_share, entity, latest_year)
    ent_first = _share(dc_share, entity, first_year)
    add("entity_share_latest", ent_latest, _pct(ent_latest), "% of electricity demand",
        DC_SHARE_FILE, f"share_pct where entity = {entity} and year = {latest_year}")
    add("entity_share_first", ent_first, _pct(ent_first), "% of electricity demand",
        DC_SHARE_FILE, f"share_pct where entity = {entity} and year = {first_year}")
    add("entity_to_world_ratio", ent_latest / world_latest, f"{ent_latest / world_latest:.1f}",
        "ratio", DC_SHARE_FILE, f"{entity} share divided by World share, latest year")

    # --- tracked AI sites (sites.csv) ------------------------------------------------
    powered = sites[sites["has_power"]]
    total_mw = float(powered["power_mw"].sum())

    add("n_sites", len(sites), f"{len(sites):,}", "sites", SITES_FILE, "Row count of sites.csv")
    add("n_countries", int(sites["country"].nunique()), f"{sites['country'].nunique():,}",
        "countries", SITES_FILE, "Distinct values in the country column")
    add("n_sites_power", len(powered), f"{len(powered):,}", "sites", SITES_FILE,
        "Rows where has_power is true (power_mw above 0)")
    add("total_mw", total_mw, _mw(total_mw), "MW of estimated IT power", SITES_FILE,
        "Sum of power_mw over sites with has_power true")

    largest = powered.loc[powered["power_mw"].idxmax()]
    add("largest_site_name", str(largest["site"]), str(largest["site"]), "text", SITES_FILE,
        "site with the largest power_mw")
    add("largest_site_mw", float(largest["power_mw"]), _mw(float(largest["power_mw"])),
        "MW of estimated IT power", SITES_FILE, "Largest power_mw")

    median_mw = float(powered["power_mw"].median())
    add("median_site_mw", median_mw, _mw(median_mw), "MW of estimated IT power",
        SITES_FILE, "Median power_mw over sites with has_power true")

    top10 = float(powered["power_mw"].nlargest(10).sum())
    add("top10_share_mw", top10 / total_mw * 100, f"{top10 / total_mw * 100:.0f}%",
        "% of tracked MW", SITES_FILE, "Sum of the 10 largest power_mw divided by total_mw")

    n_large = int((powered["power_mw"] >= LARGE_SITE_MW).sum())
    add("n_sites_ge_large", n_large, f"{n_large:,}", "sites", SITES_FILE,
        f"Count of sites with power_mw at or above {LARGE_SITE_MW}")
    add("large_site_mw", LARGE_SITE_MW, f"{LARGE_SITE_MW:,}", "MW", "facts.py",
        "Group choice (constant LARGE_SITE_MW), shown on screen as such")

    us_mw = float(powered.loc[powered["country"] == US, "power_mw"].sum())
    add("us_share_of_mw", us_mw / total_mw * 100, f"{us_mw / total_mw * 100:.1f}%",
        "% of tracked MW", SITES_FILE, "power_mw summed where country = United States, over total_mw")

    named = powered[powered["owner"] != "Unattributed"]
    top4 = float(named.groupby("owner")["power_mw"].sum().nlargest(4).sum())
    add("top4_owner_share_mw", top4 / total_mw * 100, f"{top4 / total_mw * 100:.1f}%",
        "% of tracked MW", SITES_FILE,
        "power_mw summed per named owner (Unattributed excluded), top 4, over total_mw")

    return facts
