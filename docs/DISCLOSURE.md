# Data and AI disclosure statement

Role D compiles this from the other documents. Every member checks their own part before submission.

## Data

- Sources: TODO (list from [DATA_DICTIONARY.md](DATA_DICTIONARY.md), with licences)
- Processing: `scripts/make_processed.py` regenerates every processed file from `data/raw/`. No processed file is edited by hand. TODO confirm once the script exists
- Known limits: TODO (use the "what the data cannot show" list in [BUILD_PLAN.md](BUILD_PLAN.md) section 1.5 and `content.py`)

## AI use

- Tools used: TODO (names and versions)
- Where they were used: see [PROVENANCE.md](PROVENANCE.md), one row per substantive use, with every member holding at least one row
- What was not delegated to AI: TODO

## Declaration

TODO. Draft this together and edit it until every sentence is true for every member.


## Role C individual record

- Name: Xiangqiang Ming (GitHub: yux7540-design)
- Date added: 28 October 2026
- Scope: OpenAI Codex assisted with the owner chart, site explorer, README, independent fact and interaction tests, documentation, presentation slides and speaking notes, including transition sentences.
- Verification: automated checks and their limitations are recorded in the Role C rows of [PROVENANCE.md](PROVENANCE.md). PR #9 is merged and main CI passes. Automated checks must not be described as personal manual verification.
- Live checks: Codex automated Chrome verified four rendered charts, the separate 20-site zero-power bin, the 24 sites at or above 200 MW, the unchanged owner chart and the empty-country message on 28 October 2026. See `docs/evidence/role-c-live-check-2026-10-28.json`. Owner-specific filtering, table-cell verification and the full Role B visual QA are not covered by this check.
- This name and date were added at Xiangqiang Ming's request. They identify the Role C disclosure record; they do not attest to the unresolved group declaration or to personal live-app acceptance.
