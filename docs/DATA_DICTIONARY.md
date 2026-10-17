# Data dictionary

Role A fills this in from the real files. The brief requires, for every dataset: source and URL, licence, columns and units, primary key, time coverage, latest observation, and the transform that produced it. Cover raw files and processed files. Settle the four open questions in [BUILD_PLAN.md](BUILD_PLAN.md) section 4.5 and record the answers here. `tests/test_dictionary.py` fails while any `TODO` remains.

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
| Source | Our World in Data, "Share of total electricity demand coming from data centers" (IEA and Ember data, processed by OWID). Metadata: https://api.ourworldindata.org/v1/indicators/1295514.metadata.json |
| URL | https://ourworldindata.org/grapher/data-centers-share-electricity-demand.csv?v=1&csvType=full&useColumnShortNames=true |
| Licence | CC BY for OWID's processing; the IEA and Ember inputs keep their own terms. TODO confirm both |
| Columns and units | TODO |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Retrieved on | TODO |
| Source last updated | TODO |
| Transform | None. Source copy |

## data/raw/epoch_data_center_timelines.csv (SHOULD; delete this section if chart C5 is dropped)

| Field | Value |
|---|---|
| Source | Epoch AI, AI data center timelines |
| URL | https://epoch.ai/data/data_centers/data_center_timelines.csv |
| Licence | As the Epoch file above |
| Columns and units | TODO |
| Primary key | TODO |
| Time coverage | TODO (dates include forecasts) |
| Latest observation | TODO |
| Retrieved on | TODO |
| Source last updated | TODO |
| Transform | None. Source copy |

## data/processed/dc_share.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/owid_data_centers_share_electricity_demand.csv` |
| Licence | As the raw file |
| Columns and units | See [BUILD_PLAN.md](BUILD_PLAN.md) section 4.2; TODO full units |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Transform | TODO (document each step in `scripts/make_processed.py`) |

## data/processed/sites.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/epoch_data_centers.csv` |
| Licence | As the raw file |
| Columns and units | See [BUILD_PLAN.md](BUILD_PLAN.md) section 4.2; TODO full units |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Transform | TODO (document each step, including how owner tags are stripped and how blank owners are labelled) |

## data/processed/capacity_timeline.csv (SHOULD; delete this section if chart C5 is dropped)

| Field | Value |
|---|---|
| Source | Derived from `data/raw/epoch_data_center_timelines.csv` |
| Licence | As the raw file |
| Columns and units | See [BUILD_PLAN.md](BUILD_PLAN.md) section 4.2; TODO full units |
| Primary key | TODO |
| Time coverage | TODO |
| Latest observation | TODO |
| Transform | TODO (year-end total of each site's latest power value; rows after the retrieval date are forecasts) |

## data/processed/meta.json

| Field | Value |
|---|---|
| Source | Written by `scripts/make_processed.py` |
| Columns and units | One entry per source: `url`, `licence`, `retrieved`, `source_updated` |
| Transform | TODO |
