"""Role D: the fact registry.

Every number shown inside a sentence is built here from the processed data, so each one
can be traced to a file and a computation. The list of ids is in docs/BUILD_PLAN.md section 3.5.
"""
from dataclasses import dataclass
from typing import Any

import pandas as pd

LARGE_SITE_MW = 200  # group choice; the app shows it on screen as such


@dataclass(frozen=True)
class Fact:
    id: str
    value: Any
    text: str  # how it appears on screen, for example "1.5%"
    unit: str
    source_file: str  # for example "data/processed/dc_share.csv"
    how: str  # one line describing the computation


def build_facts(dc_share: pd.DataFrame, sites: pd.DataFrame) -> dict[str, Fact]:
    """Return every fact keyed by id."""
    raise NotImplementedError("Role D: implement per docs/BUILD_PLAN.md section 3.5")
