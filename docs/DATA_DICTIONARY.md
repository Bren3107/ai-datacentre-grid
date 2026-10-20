# Data dictionary

Every raw and processed file, with the fields the brief asks for: source and URL, licence, columns and units, primary key, time coverage, latest observation, retrieval date and transform. Counts, dates and ranges were read from the downloaded files; definitions and licences come from the publishers' pages, read on 20 Oct 2026. Where something is Role A's inference rather than a publisher's statement, it says so. `tests/test_dictionary.py` fails while any field is missing or a to-do marker remains.

All three raw files were downloaded on **2026-10-20** (02:21 UTC, 13:21 in Sydney, from the HTTP `Date` header) and are committed byte for byte. `data/processed/meta.json` records each file's size and SHA-256, and `tests/test_data_contract.py` fails if a raw file changes.

Not checked: the folder layout follows BUILD_PLAN section 5.2, not the Assignment 2 Part C data-organisation standard, because that brief is not in the project folder. Brendan to confirm against it.

## Answers to the four open questions (BUILD_PLAN section 4.5)

1. **What does 0 MW mean for the 20 sites?** Epoch does not define it: the Records page defines `Current power (MW)` only as the most recent IT power value, and neither the Records nor the Methodology page mentions zero power. The Methodology page says planned data centres are included "only if those data centers have started construction". From the files: each of the 20 sites has timeline rows dated on or before 20 Oct 2026, every one of those rows shows 0 MW of IT power and 0 operational buildings, and every one of the 20 has a later-dated row with IT power above 0. So, **Role A's reading** (not stated by Epoch): 0 MW means no operational IT power recorded yet, a site under construction with power expected later. It does not mean "unknown". These sites stay in `sites.csv` with `has_power = False`, and every chart states whether it counts them.
2. **Is `Current power (MW)` facility power, and as of what date?** **No. It is IT power.** BUILD_PLAN 1.5 said facility power; that was wrong. Evidence: (a) Epoch's Records page defines it as "the most recent value for IT power capacity in megawatts, as of the current date", a lookup to the timelines `IT power (MW)` field, which covers "GPU servers, network infrastructure and storage"; facility power is the separate timelines column `Power (MW)` (IT power plus cooling, lighting and so on). (b) In the files, all 94 values equal the site's latest `IT power (MW)` dated on or before 20 Oct 2026 (sum 14,203.431374 MW in both); only 21 equal `Power (MW)`, whose sum on the same rows is 18,212.8 MW, 1.0 to 1.52 times IT power by site (mean 1.29). (c) Epoch's hub page says the 94 sites have "14.2 GW of IT power capacity" and that total facility power is 20 to 50% higher. **As of:** each site's latest record on or before the download date; those record dates run from 2025-11-16 to 2026-10-19 (93 of 94 in 2026). Wording consequence: "estimated IT power", never "facility power".
3. **Licence terms for the IEA and Ember inputs.** From OWID's indicator metadata: the two Ember inputs ("Yearly Electricity Data" and "Yearly Electricity Data Europe", 2026) are **CC BY 4.0**. The two IEA inputs ("Energy and AI", published 2025-06-16, and "Key Questions on Energy and AI", published 2026-04-16) are "(c) OECD/IEA 2024" under https://www.iea.org/terms, and the IEA product page lists the licence as its "Terms of Use for Non-CC Material". Those terms (read 20 Oct 2026) allow only insubstantial, non-commercial reproduction and say that more than 5 numerical data points must not be made available in a separate downloadable or manipulable format. OWID marks the indicator `nonRedistributable: false` and publishes this CSV itself, and our file holds derived shares (IEA numerator over Ember denominator), not the IEA's raw figures. **Not resolved:** whether our public repo may carry the 40-row file under the IEA terms is a judgement for Brendan, not something the documents settle. Options: keep it and attribute OWID, IEA and Ember (current state); or ask the unit coordinator.
4. **Is OWID's 2025 value an estimate, despite the "historical" column name?** Neither OWID (metadata and chart page) nor the IEA product page says so either way; no value is labelled estimate, projection or preliminary, and `__historical` is part of OWID's variable path. OWID's processing note calls the 2025 world share "approximately 1.5%". **Role A's inference, not verified:** the IEA input with 2025 data was published on 16 Apr 2026, so a full-year 2025 figure is likely modelled or preliminary. The app should call 2025 "the latest published value", not a measurement.

## data/raw/epoch_data_centers.csv

| Field | Value |
|---|---|
| Source | Epoch AI, "AI data centers" (documentation: https://epoch.ai/data/data-centers-documentation) |
| URL | https://epoch.ai/data/data_centers/data_centers.csv |
| Licence | Creative Commons Attribution 4.0 (CC BY 4.0): the hub page links https://creativecommons.org/licenses/by/4.0/ and says the data is "free to use, distribute, and reproduce provided the source and authors are credited" |
| Columns and units | 94 rows, 16 columns. `Name` (text, site or campus); `Current H100 equivalents` (number, compute in H100 equivalents on an 8-bit OP/s basis); `Current power (MW)` (number, megawatts of **IT power**, see question 2; 0 for 20 sites); `Current total capital cost (2025 USD billions)` (number); `Owner` (text: who owns the AI hardware, "not necessarily the owner or operator of the facility", with a trailing confidence tag `#confident`, `#likely` or `#speculative`; 9 blank, 1 untagged, 77 confident, 5 likely, 2 speculative); `Users` (text, tagged; 24 blank); `Selected Sources` (markdown links); `Calculations sheet` (URL); `Project` (77 blank); `Current chip types`, `All chip types` (comma-separated; 24 and 10 blank); `Investors`, `Construction companies`, `Energy companies` (84, 88 and 75 blank); `Country` (12 distinct; United States 77 rows); `Address` (13 blank) |
| Primary key | `Name` (94 distinct values) |
| Time coverage | A snapshot of "current" values, each site's latest record on or before the download date. Epoch covers data centres that become operational in 2024 or later (with some exceptions), and planned ones only once construction has started. Mostly United States; Epoch estimates its coverage at 44% of deployed AI compute worldwide (90% CI 30% to 79%) as of 20 Oct 2026. Not a census |
| Latest observation | Latest underlying record 2026-10-19 (from the timelines file) |
| Retrieved on | 2026-10-20 |
| Source last updated | 2026-10-19 (Epoch downloads page) |
| Transform | None. Source copy |

## data/raw/owid_data_centers_share_electricity_demand.csv

| Field | Value |
|---|---|
| Source | Our World in Data, "Share of total electricity demand used by data centers" (numerator IEA, denominator Ember, "with major processing by Our World in Data"). Metadata: https://api.ourworldindata.org/v1/indicators/1295514.metadata.json |
| URL | https://ourworldindata.org/grapher/data-centers-share-electricity-demand.csv?v=1&csvType=full&useColumnShortNames=true |
| Licence | OWID's processing CC BY 4.0; IEA inputs (c) OECD/IEA under the IEA Terms of Use for Non-CC Material (https://www.iea.org/terms); Ember inputs CC BY 4.0. See question 3 |
| Columns and units | 40 rows, 4 columns. `entity` (text, 10 values: World; United States; China; "World excl. United States and China"; and Africa, Asia Pacific, Central and South America, Europe, Middle East and North America, each suffixed "(IEA)"); `code` (text: OWID_WRL, USA, CHN; blank for the other 7); `year` (integer); `total_electricity_consumption__share_of_total_electricity_demand__historical` (number, **percent**: data-centre electricity use, including cooling and support systems, for general-purpose and AI servers, as a share of that entity's total electricity demand in that year; "does not allow a separate estimate for AI use") |
| Primary key | `entity` + `year` (40 distinct pairs) |
| Time coverage | 2020, 2023, 2024 and 2025 only; no 2021 or 2022 |
| Latest observation | 2025 (World 1.5264845%, United States 4.9384785%). See question 4 |
| Retrieved on | 2026-10-20 |
| Source last updated | 2026-06-30 (chart page "Last updated"; next update expected 2027-06-30). The indicator's metadata record was updated 2026-09-10 |
| Transform | None. Source copy |

## data/raw/epoch_data_center_timelines.csv

| Field | Value |
|---|---|
| Source | Epoch AI, "AI data center timelines" (same documentation) |
| URL | https://epoch.ai/data/data_centers/data_center_timelines.csv |
| Licence | As the Epoch file above (CC BY 4.0) |
| Columns and units | 560 rows, 14 columns. `Data center` (text, same 94 names as `Name` above); `Date` (YYYY-MM-DD, "as-of date for the status/metrics"); `Construction status` (free text); `Buildings operational` (count); `IT power (MW)` (megawatts, total IT power capacity; 1 blank); `Power (MW)` (megawatts, total facility power capacity, IT plus cooling, lighting and so on; 1 blank); `H100 equivalents` (number); `Performance (8-bit OP/s)` (integer stored as text); `Total capital cost`, `Compute cost`, `Construction cost`, `Annual operating cost` (2025 USD billions); `Water use (MGD)` (million gallons per day; 468 of 560 blank; out of scope); `Current H100 equivalents (from Data center)` (copy of the site-level value) |
| Primary key | `Data center` + `Date` (no duplicates) |
| Time coverage | 2018-12-18 to 2030-01-01. 465 rows are dated on or before the download date; 95 rows, covering 53 sites, are dated later and are forecasts (Epoch says dates come from satellite imagery, permits and company statements, and that schedules can slip or speed up) |
| Latest observation | Latest row on or before the download date: 2026-10-19 |
| Retrieved on | 2026-10-20 |
| Source last updated | 2026-10-19 (Epoch downloads page) |
| Transform | None. Source copy |

## data/processed/dc_share.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/owid_data_centers_share_electricity_demand.csv` |
| Licence | As the raw file |
| Columns and units | 40 rows. `entity` (text); `code` (text, blank for 7 entities); `year` (integer); `share_pct` (float, **percent** of that entity's electricity demand in that year) |
| Primary key | `entity` + `year` |
| Time coverage | 2020, 2023, 2024, 2025 (no 2021 or 2022) |
| Latest observation | 2025 |
| Retrieved on | 2026-10-20 (raw file) |
| Transform | `make_dc_share` in `scripts/make_processed.py`: check the four raw column names, rename the value column to `share_pct`, keep entity labels, codes and row order; nothing added, dropped or interpolated |

## data/processed/sites.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/epoch_data_centers.csv` |
| Licence | As the raw file |
| Columns and units | 94 rows. `site` (text, from `Name`); `owner` (text, `Owner` without its trailing tag, trimmed; blank becomes `Unattributed`, 9 rows); `owner_confidence` (text: `confident`, `likely` or `speculative`, empty for 10 rows: 9 blank owners and 1 untagged); `country` (text); `power_mw` (float, **estimated IT power, MW**, from `Current power (MW)`; 0 for 20 sites); `h100_equivalents` (float, H100 equivalents); `capex_usd_bn_2025` (float, 2025 USD billions); `has_power` (bool, `power_mw > 0`; 74 true) |
| Primary key | `site` |
| Time coverage | Snapshot as of 2026-10-20; per-site record dates 2025-11-16 to 2026-10-19 |
| Latest observation | 2026-10-19 |
| Retrieved on | 2026-10-20 (raw file) |
| Transform | `make_sites` in `scripts/make_processed.py`: one output row per raw row, in raw order. Owner: trim, take a trailing `#word` into `owner_confidence` (regular expression `#(\w+)$`), remove it and trim again, then replace an empty owner with `Unattributed`. Rename the other columns as listed and add `has_power`. No row is dropped, so 0 MW sites stay |

## data/processed/capacity_timeline.csv

| Field | Value |
|---|---|
| Source | Derived from `data/raw/epoch_data_center_timelines.csv` |
| Licence | As the raw file |
| Columns and units | 11 rows. `year_end` (date, YYYY-12-31); `power_mw_total` (float, megawatts of **estimated IT power**, summed over sites); `is_forecast` (bool, true when `year_end` is after the retrieval date 2026-10-20, so from 2026-12-31); `n_sites` (integer, sites with IT power above 0 at that date) |
| Primary key | `year_end` |
| Time coverage | 2019-12-31 to 2029-12-31. One raw row dated 2030-01-01 (Stream Phoenix) falls outside the series |
| Latest observation | Last observed year-end 2025-12-31: 6,774.32971 MW at 46 sites. Later year-ends are forecasts |
| Retrieved on | 2026-10-20 (raw file) |
| Transform | `make_capacity_timeline` in `scripts/make_processed.py`: drop the one row with no IT power value; for each year-end, take each site's latest row dated on or before it and sum `IT power (MW)` (a step function: a site keeps its last stated value until a later row changes it). IT power is used so the series matches `sites.csv`. Built-in check (card C5): the same sum at the retrieval date is 14,203.431374 MW, equal to the `sites.csv` total (difference 0, stored in `meta.json`) |

## data/processed/meta.json

| Field | Value |
|---|---|
| Source | Written by `scripts/make_processed.py` from constants in that script and the raw file bytes |
| Licence | Not applicable (metadata; the sources' licences are recorded inside it) |
| Columns and units | One object per source (`epoch_data_centers`, `owid_data_centers_share`, `epoch_data_center_timelines`) with `url`, `licence`, `retrieved` and `source_updated` (dates, YYYY-MM-DD), `raw_file`, `raw_bytes` and `raw_sha256`. A `checks` object holds the timeline IT power total at the retrieval date, the `sites.csv` total and their difference (MW) |
| Primary key | Source key |
| Time coverage | Not applicable |
| Latest observation | Not applicable |
| Retrieved on | 2026-10-20 for all three raw files |
| Transform | `retrieved` and `source_updated` are typed into the script when files are downloaded (the only manual input apart from the raw files); sizes, hashes and `checks` are computed |
