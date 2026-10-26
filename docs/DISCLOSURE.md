# Data and AI disclosure statement

Role D compiles this from the other documents. Every member checks their own part before submission.

## Data

- Sources, all public and citable, retrieved on 20 October 2026 (details, keys, units and dates in [DATA_DICTIONARY.md](DATA_DICTIONARY.md)):
  - Epoch AI, AI data centers and AI data center timelines. Licence: Creative Commons Attribution 4.0 (CC BY 4.0). Raw files: `data/raw/epoch_data_centers.csv` and `data/raw/epoch_data_center_timelines.csv`. Epoch last updated them on 19 October 2026.
  - Our World in Data, share of total electricity demand used by data centers (OWID processing CC BY 4.0, Ember inputs CC BY 4.0, IEA inputs under the IEA Terms of Use for Non-CC Material). Raw file: `data/raw/owid_data_centers_share_electricity_demand.csv`. OWID last updated it on 30 June 2026.
- Processing: `scripts/make_processed.py` regenerates every processed file in `data/processed/` from `data/raw/`. No processed file is edited by hand, and `tests/test_regeneration.py` checks that running the script leaves the processed files unchanged. Every number on the page is computed in `facts.py` from the processed files, and the page lists each one with its source file and calculation in the "Trace a number" box.
- Known limits (the page shows these in "What these data cannot show"):
  - Neither source shows whether any particular grid is under strain.
  - The share file covers all data centres, not only AI.
  - Epoch tracks major sites and its coverage began in the United States, so country shares describe what Epoch tracks, not the world.
  - Epoch's megawatts are estimated IT power, which leaves out cooling and other overhead.
  - The share file has no values for 2021 and 2022, and the sources do not say whether the 2025 value is preliminary.
  - Whether the IEA terms allow a public repository to carry the IEA-derived OWID file is not settled (see the dictionary).
  - The 200 MW large-site threshold is a choice made by our group, not a figure from the sources.

## AI use

- Tools used, as recorded in [PROVENANCE.md](PROVENANCE.md):
  - Brendan: Claude Code (Claude Sonnet 5.5 for the scaffold; Claude Opus 5.5 for the data pipeline, dictionary and country chart).
  - Daniel: Claude in claude.ai (Claude Opus 5.5) for the trend chart and its tests.
  - yux7540-design: OpenAI Codex for the owner chart, site explorer, README and independent checks.
  - Avishek: Claude in claude.ai (Claude Sonnet 5.5) for the page, wording and fact registry.
- Where they were used: see [PROVENANCE.md](PROVENANCE.md), one row per substantive use, each with the check applied to the result.
- What was not delegated to AI:
  - The group chose the question, the persona and the energy-only scope in its own discussion.
  - The group chose the 200 MW large-site threshold, and the page says so.
  - Each member decided whether to accept their own AI output, recorded in the Outcome column of the matrix.

## Declaration

We used AI tools as listed above and in [PROVENANCE.md](PROVENANCE.md). Each member has recorded what they asked, what came back and the check applied, and each member is responsible for understanding and explaining their own part. The data are public and cited, no processed file is edited by hand, and every number shown on the page is computed from the files in `data/`.

Each member confirms that the AI use recorded for their own part is complete and true:

- Brendan: confirmed ______ (date)
- Daniel: confirmed ______ (date)
- yux7540-design: confirmed ______ (date)
- Avishek: confirmed ______ (Oct 26 2026)
