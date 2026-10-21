# Is AI data-centre growth a grid problem, or still a small share of electricity demand?

Assignment 3: The Rise of Artificial Intelligence — Data Narrative Studio.
An interactive Streamlit narrative using public, citable data.

## Persona and decision

Priya is a regional energy planner at a transmission or state energy agency. She must decide whether data-centre load deserves priority in grid planning now, or can be monitored for another planning cycle.

## User stories and walk-throughs

1. As a regional energy planner, I want to see how data centres' share of electricity demand has changed since 2020, so that I can assess whether the load is still marginal where I plan.
   Walk-through: choose World or Country or region in Scale, then select Regions in Story 1; compare the trend panels and their Show the numbers table.
2. As a regional energy planner, I want to see which countries and owners hold the tracked AI data-centre capacity, so that I can judge how concentrated the tracked load is.
   Walk-through: go to Story 2, compare the country share bar and owner ranking, and expand Show the numbers. These whole-dataset charts remain fixed when Story 3 filters change.
3. As a regional energy planner, I want to filter tracked sites by country, owner and size, so that I can inspect how much capacity sits in a few very large sites.
   Walk-through: in Story 3 select Countries and Owners, change Minimum IT power (MW), and optionally enable Include sites reporting 0 MW; the size distribution and Largest sites in this selection table update together.

## Charts and Visual Vocabulary families

| Chart | Task | Family | Form |
|---|---|---|---|
| C1: Electricity-demand share | Compare regional levels and changes | Change over time | Line charts in small multiples |
| C2: Tracked IT power by owner | Compare the largest named owners | Ranking | Ordered horizontal bars |
| C3: Tracked IT power by country | Compare shares of the tracked total | Part-to-whole | One 100% stacked bar |
| C4: Site sizes | Show counts in size bands | Distribution | Bars in 100 MW bands |

C2 shows the top eight named owners, followed by All other named owners and Unattributed. Percentages include both catch-all groups in the denominator. C2 always uses the whole dataset, excluding sites at 0 MW.

C4 uses lower-inclusive, upper-exclusive bands. Labels such as 0–99 abbreviate [0, 100), so 99.9 belongs in that band. Bands extend beyond 999 MW as needed. Selected 0 MW sites appear in a separate bar, never twice. All countries and owners are initially selected; clearing either picker gives an explanatory empty state. The minimum threshold applies even when the zero-power checkbox is on.

## Data and interpretation

Source snapshots are in `data/raw/`; reproducible app inputs are in `data/processed/`. See [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for provenance, units, licences, keys, dates and transforms.

Important correction to the original build plan: Epoch's `Current power (MW)` is **estimated IT power**, not total facility power. It excludes cooling and other facility overhead. Owner means the listed hardware owner, not necessarily the facility owner or operator. Country shares describe Epoch's coverage, not the entire world. OWID covers all data centres, not only AI, and has observations for 2020 and 2023–2025 only. Neither source demonstrates local grid strain or causation. The dictionary records unresolved questions about IEA redistribution terms and the status of the 2025 value.

## Run locally

Use Python 3.13 with the pinned dependencies:

```sh
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python scripts/make_processed.py
python -m pytest -q
python -m streamlit run app.py
```

## Integration status

Role A's data and country chart are available. Role C provides `charts.owners.render(sites)` and `charts.sites.render(sites)` for Role D to call in Stories 2 and 3. Chart builders return a Plotly Figure, or None for empty inputs. The main page, Scale lens and trend chart are still awaiting their owners' implementations at this branch's creation; the walk-throughs above specify the intended integrated experience. No verified deployed URL has yet been provided.

`tests/test_facts.py` independently computes the expected registry from processed files using Python's standard library. It marks the unimplemented Role D registry as an expected failure; that is pending integration, not a verified fact registry. Once implemented, missing IDs, incorrect values and missing traceability fail normally. Dynamic entity facts await Role D's entity-selection interface.

## AI provenance and disclosure

See [PROVENANCE.md](docs/PROVENANCE.md) and [DISCLOSURE.md](docs/DISCLOSURE.md). Each member records their actual AI use and a verification that could have failed. The project-wide disclosure remains Role D's responsibility.
