# Data dictionary

Role A fills this in from the real files. The brief requires, for every dataset: source and URL, licence, columns and units, primary key, time coverage, latest observation, and the transform that produced it. Cover raw files and processed files.

## data/raw/epoch_data_centers.csv

| Field | Value |
|---|---|
| Source | Epoch AI, AI data centers (documentation: https://epoch.ai/data/data-centers-documentation) |
| URL | https://epoch.ai/data/data_centers/data_centers.csv |
| Licence | Creative Commons Attribution (confirm the version on the Epoch page) |
| Columns and units | TODO |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Retrieved on | TODO |
| Source last updated | TODO |
| Transform | None. Source copy |

## data/raw/owid_data_centers_share_electricity_demand.csv

| Field | Value |
|---|---|
| Source | Our World in Data, "Share of total electricity demand coming from data centers" (IEA and Ember data, processed by OWID) |
| URL | https://ourworldindata.org/grapher/data-centers-share-electricity-demand.csv?v=1&csvType=full&useColumnShortNames=true |
| Licence | CC BY for OWID's processing; the IEA and Ember inputs keep their own terms. TODO confirm both |
| Columns and units | TODO |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Retrieved on | TODO |
| Source last updated | TODO |
| Transform | None. Source copy |

## data/processed/dc_share.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/owid_data_centers_share_electricity_demand.csv` |
| Licence | As the raw file |
| Columns and units | See "Data contracts" in [TEAM_PLAN.md](TEAM_PLAN.md); TODO full units |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Transform | TODO (document each step in `scripts/make_processed.py`) |

## data/processed/sites.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/epoch_data_centers.csv` |
| Licence | As the raw file |
| Columns and units | See "Data contracts" in [TEAM_PLAN.md](TEAM_PLAN.md); TODO full units |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Transform | TODO (document each step, including how owner tags are stripped) |

## data/processed/meta.json

| Field | Value |
|---|---|
| Source | Written by `scripts/make_processed.py` |
| Columns and units | One entry per source: `url`, `licence`, `retrieved`, `source_updated` |
| Transform | TODO |
