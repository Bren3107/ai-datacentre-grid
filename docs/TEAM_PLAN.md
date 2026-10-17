# Team plan

Question: **Is AI data-centre growth a grid problem, or still a small share of electricity demand?**

Four people, four roles. Each role owns its own files, so branches rarely collide.

## Ground rules

These mirror what the marking checks look at.

1. Write, commit and push your own part from your own GitHub account. Nobody pushes work on someone else's behalf.
2. AI help is allowed. Log every substantive use as your own row in [PROVENANCE.md](PROVENANCE.md), with a check that could have failed (for example, recomputing a number by hand and comparing it with the app).
3. In your recording you show your own part, defend one design decision and trace one displayed number to its source file. Keep only what you can explain.
4. Every number on screen comes from the data package. No figures typed by hand into the app.

## Dates

| When | What |
|---|---|
| Mon 19 Oct | Role A pushes the raw and processed data; contracts below confirmed |
| Tue 20 Oct | Every chart merged into main; deployed URL works |
| Thu 22 Oct (night) | Recordings finished and submitted. The deadline is Fri 23 Oct, 11:59pm |
| Fri 6 Nov | Peer feedback forms done for every other member |
| Fri 13 Nov | Feature freeze; run through all 30 checks |
| Fri 20 Nov, 11:59pm | Portfolio PDF: app URL, repo URL, commit hash or tag |

## Roles

### Role A: Data and delivery

Files: `scripts/make_processed.py`, `data/`, `docs/DATA_DICTIONARY.md`, `charts/geo.py`, `requirements.txt`

- Download the two source files into `data/raw/` and note the retrieval date.
- Write `scripts/make_processed.py` so the processed files regenerate from the raw ones (schemas below). Strip the confidence tags from owner names and document the rule.
- Fill `docs/DATA_DICTIONARY.md` for every raw and processed file.
- `charts/geo.py`: capacity (MW) by country.
- Deploy on Streamlit Community Cloud, check the URL loads in under 5 seconds, and tag the release that gets submitted.

Recording: trace one displayed number back to the raw file, and defend the form of the country chart.

### Role B: Trend and QA

Files: `charts/trend.py`

- `charts/trend.py`: data-centre share of electricity demand by region over time, with a region selector. Label the values on the chart. State units, baseline and time coverage (including the gap years) in the caption.
- An empty selection shows a message, not an error.
- QA across the whole app: 1366x768 with vertical scrolling only; a colour-blind check (Chrome DevTools, Rendering tab, Emulate vision deficiencies); walk each user story end to end.

Recording: defend the form of the trend chart and the selector, and show the QA findings you fixed.

### Role C: Sites

Files: `charts/sites.py`

- Ranking chart of owners by total MW.
- Scatter of capital cost against MW (or H100 equivalents against MW).
- Filters: country, owner, minimum MW. An empty result shows a message, not an error.
- Decide and state in the caption how sites reporting 0 MW are treated.

Recording: defend the ranking and scatter forms and the filters, and trace one displayed number to the raw file.

### Role D: Story and shell

Files: `app.py`, `charts/headline.py`, `README.md`, `docs/DISCLOSURE.md`, `docs/PROVENANCE.md` (compiling)

- Opening screen: the question plus a headline fact computed from the data (stat tiles and one comparison chart in `charts/headline.py`).
- A stated answer in text, and a "what the data cannot show" section (starting list below).
- Footer with sources and the last data refresh, read from `data/processed/meta.json`.
- README: persona and decision, and three user stories (finalise the draft below with the group).
- Disclosure statement, and keep the provenance matrix complete (every member has a row) before submission.
- Until Role A pushes data, build against the schemas below with throwaway fake rows that never get committed.

Recording: defend the choice of opening fact and the headline visual.

### Everyone

- At least one provenance row, written by you.
- A branch and pull request for your files.
- Your own 5-minute recording (covers: question and persona, your part on screen, one design decision with the rejected alternative, one number traced to source, your AI use and its check).
- Peer feedback on every other member's recording.

## Data contracts

Fixed up front so B, C and D can build before Role A finishes. Role A confirms or changes these by Mon 19 Oct and tells the group. The raw column names below came from a web read of the two source pages, so Role A checks them against the downloaded files.

### data/processed/dc_share.csv

Source: Our World in Data CSV for "Share of total electricity demand coming from data centers" (IEA and Ember data).

| Column | Type | Meaning |
|---|---|---|
| entity | text | Region or country label as in the source, for example "World" or "United States" |
| code | text | ISO code where the source has one, else empty |
| year | integer | On first read the source had 2020, 2023, 2024 and 2025; 2021 and 2022 were absent |
| share_pct | number | Data-centre electricity use as a percent of total electricity demand. Role A confirms the unit against the OWID metadata |

### data/processed/sites.csv

Source: Epoch AI data centres CSV.

| Column | Type | Meaning |
|---|---|---|
| site | text | `Name` |
| owner | text | `Owner` with confidence tags (such as #confident) stripped. Role A documents the rule |
| country | text | `Country` |
| power_mw | number | `Current power (MW)` |
| h100_equivalents | number | `Current H100 equivalents` |
| capex_usd_bn_2025 | number | `Current total capital cost (2025 USD billions)` |
| has_power | true/false | `power_mw > 0`. Some sites report 0 MW; each chart owner states how those are treated |

### data/processed/meta.json

One entry per source with `url`, `licence`, `retrieved` (the date it was downloaded) and `source_updated` (the date the source page gives). Role D reads it for the sources and last-refresh line.

### Chart modules

Each module exposes `render(...)` and `app.py` calls it.

| Module | Call | Owner |
|---|---|---|
| `charts/headline.py` | `render(dc_share, sites)` | D |
| `charts/trend.py` | `render(dc_share)` | B |
| `charts/sites.py` | `render(sites)` | C |
| `charts/geo.py` | `render(sites)` | A |

Use `theme.py` for colours (colour-blind-safe palette) and `apply_layout` for titles and axis labels.

## What the data cannot show (starting list for Role D)

- Local grid stress: neither file has grid capacity, reserve margins or local demand.
- AI-only use: the OWID share covers all data centres, not AI alone.
- Coverage: the Epoch file lists major AI data centres, not every data centre.
- Time: the OWID series has gaps, and the Epoch sites file is a snapshot.

These come from the source pages. Confirm each against the files before it goes on screen.

## Draft persona and stories (the group edits and agrees these)

Persona: Priya, a regional energy planner at a transmission or state energy agency. Decision: whether data-centre load deserves priority in grid planning now, or can be monitored for another planning cycle.

1. As a regional energy planner, I want to see data centres' share of electricity demand by region since 2020, so that I can tell whether the load is still marginal where I plan.
2. As a regional energy planner, I want to see which owners and countries hold the most AI data-centre capacity (MW), so that I can judge how concentrated the new load is.
3. As a regional energy planner, I want to filter sites by country, owner and minimum size, so that I can see how much capacity sits in a few very large sites.

## Marking map

| Criterion | Main owners |
|---|---|
| Question, persona, stories | D (README, opening screen); B walks each story |
| Analytical quality | Each chart owner for captions, units and baselines; D for the stated answer and limits; A for traceability |
| Visual form | Each chart owner for their charts; B for the colour-blind check |
| The app works | A (deploy, load time); B (layout, empty states); B and C (interactions); D (opening screen, footer) |
| Data package and process | A (data folder, dictionary, regeneration, commit hash); everyone (provenance row); D (disclosure) |

## Git workflow

```bash
git clone https://github.com/Bren3107/ai-datacentre-grid.git
cd ai-datacentre-grid
git switch -c feature/<role>-<your-name>
# edit only your files, then
git add <your files>
git commit -m "Role B: trend chart"
git push -u origin feature/<role>-<your-name>
```

Open a pull request on GitHub, get one other member to review it, and Role A merges. Run `git pull` before you edit `docs/PROVENANCE.md`, and add your rows at the end of the table.

## Risks to check early

- Streamlit Community Cloud apps can go to sleep when unused, and waking one can take longer than 5 seconds. Role A checks this and opens the app shortly before assessment.
- `requirements.txt` pins the versions installed on Brendan's machine (Python 3.13.5). Pick the same Python version when deploying, and relax the pins if the install fails.

## Optional stretch (not needed for the 30 checks)

Convert site MW into annual TWh and compare it with national electricity demand. This needs an extra dataset and a stated load-factor assumption, so skip it unless Roles A to D are finished early.
