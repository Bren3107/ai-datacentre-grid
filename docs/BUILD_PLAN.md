# Build plan: "Is AI data-centre growth a grid problem, or still a small share of electricity demand?"

The single set of instructions for all four roles, agreed 18 Oct 2026. Read sections 1 to 4 once, then your role card in section 6. Section 8 maps all 30 marking checks to who builds and who verifies them.

## Settled design calls

1. **One scrolling page, wide layout, no sidebar, light theme forced.** Simplest for the 1366x768 check and for "opens on something true".
2. **Signature interaction: the scale lens** (World / Country or region / Site). The verdict sentence changes with the scale. It is the app's argument: the same data supports "small" and "a planning problem".
3. **Four core charts, four Visual Vocabulary families, plus one optional.** Change over time, part-to-whole, ranking, distribution (+ optional forecast timeline).
4. **No map and no scatter.** A map adds load time and cannot label every value; a 74-point scatter cannot either.
5. **Label every value, and give every chart a "Show the numbers" table.** The brief's "readable without hovering" check overrides the dataviz skill's "label selectively" rule. The skill's palette, mark and anti-pattern rules still apply.
6. **Every number in a sentence comes from code** (`facts.py`), never from a hand-typed figure, and every sentence lives in one file (`content.py`) so claims can be reviewed in one place.
7. **The verdict is scale-dependent**, with the judgement labelled "Our reading" and kept apart from the numbers.
8. **Palette: validated subset of Okabe-Ito**, yellow and black removed (yellow fails the lightness band; see section 3.3). This replaced the palette in the first scaffold.
9. **Water is out of scope.** (The timelines file has a `Water use (MGD)` column; it is a stretch idea only.)
10. **Tests plus CI** (pytest on GitHub Actions), because they produce the "check that could have failed" evidence the provenance matrix needs.
11. **Deploy on Streamlit Community Cloud on Monday**, not the last day, with a scheduled keep-alive (efficacy unverified) and manual visits as the fallback.
12. **No custom fonts in the 30-checks phase.** Built-in font; custom type is a COULD.

## 1. Design

### 1.1 Intent
Show an energy-planning reader that the answer to "grid problem or small share?" **depends on the scale you ask at**, using only public data, with every number traceable to a file. The same data supports both readings, which makes the question arguable by construction.

**Persona:** Priya, a regional energy planner at a transmission or state energy agency. **Decision:** whether data-centre load deserves priority in grid planning now, or can be monitored for another planning cycle.

### 1.2 Goals, non-goals, anti-goals
- **Goals:** (G1) pass all 30 checks with evidence for each; (G2) one clear, scale-dependent answer that stays inside the data; (G3) every number traceable; (G4) each member owns a real, explainable part; (G5) cold load under 5 s and no horizontal scroll at 1366x768.
- **Non-goals:** forecasting; water; grid-stress modelling; maps; multi-page navigation; extra datasets before 13 Nov; causal claims.
- **Anti-goals (failure even if it runs):** a claim the data cannot support ("AI is straining grids"); a hand-typed number; an unlabelled or tooltip-only chart; one person's commits; the app asleep when marked.

### 1.3 Constraints from the brief
Streamlit app with a public URL and a GitHub repo; public, citable data; for any number on screen, name the file and the transform; Part 1 recording is individual; AI use goes in the provenance matrix and disclosure; the group mark is scaled by a peer contribution factor checked against recordings and commit history.

### 1.4 The answer the app gives (draft; the group agrees the wording on Mon 19 Oct)
> **Our answer: it depends on the scale.** Across the world, data centres used {world_share_latest} of electricity demand in {latest_year}, which is still small. In the United States the share was {us_share_latest}, {us_to_world_ratio} times the world figure, and {n_sites_ge_large} of the {n_sites_power} tracked AI sites are estimated to draw {large_site_mw} MW or more each. These data cannot show whether any particular grid is under strain.

Placeholders are filled by `facts.py`. The `large_site_mw` threshold (200) is a group choice and is shown on screen as such.

### 1.5 Data facts that shape the design
*Read on 18 Oct from web pages and files; Role A re-derives every one from the downloaded files before it reaches the app.*

| Fact | Source of the fact | Design consequence |
|---|---|---|
| OWID share file: 10 entities (World, United States, China, "World excl. United States and China", and 6 IEA regions), years **2020, 2023, 2024, 2025 only**, 40 rows, 1,511 bytes, values in percent | CSV read verbatim | C1 must show the 2021-2022 gap; caption states it |
| World share 1.01% (2020) to 1.53% (2025); United States 2.64% to 4.94% (3.2x world in 2025); China 0.80% to 1.11%; Europe (IEA) 1.44% to 1.87%; Middle East (IEA) 0.09% to 0.28% | same CSV | Lens World and Country use these. The Middle East jump in 2025 is large; do not interpret it |
| OWID definition: all data-centre electricity use including cooling and support, general-purpose and AI servers; "does not allow a separate estimate for AI use" | OWID metadata | Never write "AI uses X%". Say "data centres" for OWID |
| OWID updated 30 Jun 2026; sources IEA (2025, 2026) and Ember (2026) | OWID metadata | Footer cites both; licence of IEA and Ember inputs still to confirm (Role A) |
| Epoch `data_centers.csv`: 94 rows, 16 columns; 12 countries; 77 rows United States; **20 rows report 0 MW**; owner text carries tags (`#confident`, `#likely`, `#speculative`); **9 owners blank** | web transcription of 4 columns, not the file | Processing rules in 4.2; "Unattributed" bucket |
| Indicative aggregates from that transcription: 74 sites above 0 MW, about 14,076 MW total, United States about 84% of it, Malaysia 8%, China 5%; Google 22.6%, Meta 15.9%, Amazon 12.4%, Microsoft 10.8% (about 62% together), Unattributed 11.6%; top 10 sites 38%; median site about 152 MW; 24 sites at or above 200 MW; 3 at or above 500 MW; largest 946 MW | computed from the transcription | **Do not copy any of these into the app.** `facts.py` computes them from the real file |
| Epoch's hub began United States only and widened; MW is estimated *facility* power (about 1.3x IT power), from satellite imagery of cooling plant plus permits | Epoch article | Country shares reflect Epoch's coverage, not the world. Say "estimated facility power" |
| Epoch `data_center_timelines.csv`: 14 columns, a site at a date, dates from 2018 to **2029 including forecasts**, includes `Water use (MGD)` | web read, truncated | C5 must separate "to date" from "forecast" |

## 2. Creative direction (one page)

**Concept: a load report.** Plain, exact and quietly confident, like a utility's load report. Subject vernacular: nameplates and meter readings, so every number carries its unit and period. Boldness is spent in one place, the **scale lens**; everything else stays quiet.

**Tokens** (contrast ratios computed against the paper colour, WCAG)

| Token | Hex | Use | Contrast on paper |
|---|---|---|---|
| Paper | `#FCFCFB` | page background | n/a |
| Band | `#EEF3F8` | lens band, notes column | n/a |
| Ink | `#14233A` | all text | 15.4 |
| Ink-2 | `#4B5A6E` | secondary text, "other" series | 6.9 |
| Muted | `#5A6678` | captions | 5.7 (5.2 on band) |
| Blue | `#0072B2` | World, single-series bars | 5.1 |
| Vermillion | `#D55E00` | United States, the focus entity (marks only; text use `#B04A00`, 5.4) | 3.8 |
| Green | `#009E73` | China (marks only) | 3.3 |
| Context grey | `#7D8796` | Other, Unattributed (marks only) | 3.5 |
| Grid | `#D9DEE5` | hairlines | n/a |

Colour follows the entity everywhere: World blue, United States vermillion, China green; all other entities ink-2 or grey. Text never takes a data colour. Orange `#E69F00`, sky `#56B4E9` and purple `#CC79A7` pass the validator but sit below 3:1 on paper; reserve them and use only with labels.

**Type:** Streamlit's built-in sans for everything. Scale: title 2.25rem, lens hero figure 3rem (proportional figures), section heads 1.5rem, body 1rem, captions 0.875rem. Tabular figures only inside tables.

**Layout:** question band, lens band, three story bands each with a chart (left, 8/12) and a margin-notes column (right, 4/12) holding what it shows, unit, period, source. Then answer-limits-other-side, then the footer. No cards, shadows, icons, emoji, all-caps labels or arrows.

**Review against generic defaults (what changed):** dropped cream paper with a serif and terracotta; dropped near-black with an acid accent; replaced the four KPI tiles with one hero figure inside the lens; no eyebrow labels; no monospace data labels; margin notes instead of boxed cards.

**Motion:** none. Plotly transitions off. Nothing animates on load.

**Wireframe at 1366 wide (ASCII)**
```
+----------------------------------------------------------------------+
| Is AI data-centre growth a grid problem, or still a small share of   |
| electricity demand?                                                  |
| {n_sites} tracked AI data centres in {n_countries} countries, plus   |
| IEA share-of-demand data 2020-2025.  Written for a regional planner. |
| Our answer: it depends on the scale. ... (computed, 3 sentences)     |
+----------------------------------------------------------------------+
| Scale  [ World | Country or region | Site ]   [picker if Country]    |
|  1.5%                | Data: ... up from 1.0% in 2020 ...            |
|  of world demand,    | Our reading: at this scale the load is        |
|  2025                |   still small.                                |
+----------------------------------------------------------------------+
| Story 1  Is the load still marginal where I plan?                    |
| [Regions: multiselect]                                               |
| +-- C1 small multiples, 2 x 2 -----------+ +-- notes ---------------+ |
| |                                        | | What it shows          | |
| +----------------------------------------+ | Unit / Period / Source | |
| [Show the numbers]                         +------------------------+ |
+----------------------------------------------------------------------+
| Story 2  Who holds the capacity?                                     |
| +-- C3 country, one 100% bar -------------+ +-- notes --------------+ |
| +-- C2 owners, ordered bars --------------+ +-- notes --------------+ |
+----------------------------------------------------------------------+
| Story 3  How much sits in a few very large sites?                    |
| [Country] [Owner] [Minimum MW] [Include 0-MW sites]                  |
| +-- C4 site-size bars --------------------+ +-- notes --------------+ |
| Largest sites in this selection (table)                              |
+----------------------------------------------------------------------+
| What these data cannot show  |  The other side of the argument       |
+----------------------------------------------------------------------+
| Sources, licences, last refresh.   [Trace a number]                  |
+----------------------------------------------------------------------+
```

## 3. App specification

### 3.1 Page flow and owners
| Block | File | Owner |
|---|---|---|
| Title, sub-line, "Our answer", story links, footer, assembly | `app.py` | D |
| Scale lens | `app.py` (function `render_lens`) | D |
| All sentences | `content.py` | D |
| Fact registry | `facts.py` | D |
| Theme tokens, `apply_layout` | `theme.py`, `.streamlit/config.toml` | D |
| C1 trend | `charts/trend.py` | B |
| C5 forecast timeline (SHOULD) | `charts/timeline.py` | B |
| C3 country | `charts/country.py` | A |
| C2 owners | `charts/owners.py` | C |
| Story 3 filters, C4, largest-sites table | `charts/sites.py` | C |

### 3.2 The scale lens (exact behaviour)
`st.segmented_control("Scale", ["World", "Country or region", "Site"], default="World", required=True)`. If it ever returns `None`, treat it as World. "Country or region" shows a `st.selectbox` of the 8 OWID entities other than "World" and "World excl. United States and China" (default United States).

| Lens | Hero figure and label | Data sentence | Our-reading sentence |
|---|---|---|---|
| World | `{world_share_latest}` "of world electricity demand went to data centres in {latest_year}" | "Up from {world_share_first} in {first_year}. The figure covers all data centres, not only AI." | "Our reading: at this scale the load is still small." |
| Country or region | `{entity_share_latest}` "of {entity}'s electricity demand went to data centres in {latest_year}" | "That is {entity_to_world_ratio} times the world share, up from {entity_share_first} in {first_year}." | by ratio: 2 or more "large enough to matter for planning"; 1 to under 2 "above the world average"; under 1 "below the world average", each prefixed "Our reading: at this scale the load is ..." |
| Site | `{largest_site_mw} MW` "estimated facility power of the largest tracked AI data centre, {largest_site_name}" | "The median tracked site is {median_site_mw} MW. The ten largest hold {top10_share_mw} of the {total_mw} MW tracked, and {n_sites_ge_large} sites are at or above {large_site_mw} MW." | "Our reading: at this scale single sites are large loads. Whether a local grid can carry one is outside these data." |

The ratio-to-reading rule is a function with a unit test for each branch (a check that can fail).

### 3.3 Chart cards
Every chart: title, axis titles with units, labelled values, a caption in the notes column with **What it shows / Unit / Period / Source**, a "Show the numbers" expander (`st.dataframe`), colours only from `theme.py`, `transition_duration=0`, height 420 or less per panel row. Each builder is a pure function returning a Plotly `Figure` (or `None` when empty) so tests can check it without Streamlit.

**C1: Data centres' share of electricity demand, 2020 to 2025 (Role B)**
- Task: show how the share changed in each region and compare levels. Family: **change over time**. Form: line with markers, **small multiples** (2 columns, one panel per selected region, shared y-axis).
- Data: `dc_share.csv`. x = year (ticks 2020, 2023, 2024, 2025 only), y = `share_pct`. Shade 2021 to 2022 grey with the label "No data".
- Colours: World blue, United States vermillion, all others ink-2.
- Labels: every point, ink text, one decimal and a % sign, above the marker. Pad the y-range so no label clips.
- Axis titles: "Year", "Share of electricity demand (%)".
- Interaction: `st.multiselect("Regions", all_entities, default=[World, United States, China, Europe (IEA)], max_selections=6)`. Empty selection shows `st.info("Pick at least one region to draw the chart.")`.
- Caption: "Data centres' share of each region's total electricity demand. Unit: % of that region's demand in that year. Period: 2020 and 2023 to 2025; no data for 2021 and 2022. Covers all data centres, not only AI. Source: IEA 'Energy and AI' and Ember, via Our World in Data, retrieved {retrieved}."
- Rejected alternative: one multi-line chart (World, China and Europe sit within 0.3 to 0.6 points of each other, so labels collide and identity relies on colour). Fallback if the facets look bad: one panel with World plus one chosen region.
- Test: title present; both axis titles contain "(%)"; one text label per point; empty selection returns `None`.

**C2: Tracked AI data-centre power by owner (Role C)**
- Task: show who holds the capacity. Family: **ranking**. Form: horizontal ordered bars, top 8 named owners, then "All other named owners" and "Unattributed" at the bottom in grey.
- Data: `sites.csv`, sites with `power_mw` above 0, summed by `owner`. Whole dataset, not filtered.
- Labels: at the bar end, "3,179 MW (22.6%)" style. Axis titles: "Estimated facility power (MW)", "Owner". Bars blue, grey for the two catch-all rows; bar thickness 24 px or less.
- Caption: "Estimated facility power of tracked AI data centres, summed by listed owner. Unit: megawatts (MW). Period: as of {retrieved}. Owner is as listed by Epoch; blank owners are shown as Unattributed. Source: Epoch AI, AI data centers."
- Rejected alternative: pie or donut (close values, anti-pattern) and treemap (small labels clip).
- Test: bars sorted descending apart from the two grey rows; the labelled percentages sum to 100 (within rounding).

**C3: Where tracked AI data-centre power is located (Role A)**
- Task: show how location concentrates the load. Family: **part-to-whole**. Form: one 100% stacked horizontal bar: top 3 countries by MW plus "Other countries (n)".
- Colours: United States vermillion, China green when it is in the top 3, other named countries ink-2, Other grey; 2 px gaps between segments. Labels inside segments of 8% or more; the legend lists every segment with its value ("United States 84.2%") so small segments stay readable.
- Axis title: "Share of tracked estimated facility power (%)". Hide the y-axis.
- Caption includes: "Countries reflect what Epoch tracks (its coverage began in the United States), not the world."
- Rejected alternative: map (load time, cannot label every value) and pie (anti-pattern).
- Test: segments sum to 100; legend text contains every value.

**C4: How big are the tracked sites? (Role C)**
- Task: show how lumpy the load is. Family: **distribution**. Form: bars of site counts in 100 MW bins (0 to 99, 100 to 199, ... 900 to 999; left-closed), built with `pandas.cut` and drawn with `px.bar`, count labelled above each bar.
- Scoped by the Story 3 filter row. Toggle on "Include 0-MW sites" adds a separate "0 MW" bar at the left.
- Axis titles: "Estimated facility power per site (MW)", "Number of sites".
- Below it: **Largest sites in this selection**, a table of the 10 biggest (site, owner, country, MW).
- Empty state: `st.info("No tracked sites match these filters. Lower the minimum size, add a country or owner, or clear the filters.")`.
- Rejected alternatives: box plot (hides counts), density curve (implies values between observations), dot strip of 74 points (cannot label every point).
- Test: bin counts sum to the number of filtered sites; empty filter returns `None`.

**C5: Tracked capacity to date and forecast (Role B, SHOULD)**
- Task: show growth and how much is still a forecast. Family: **change over time**. Form: line with markers at year-end, 2019 to 2029, solid up to the retrieval year and dashed after (dashed reads as projection here, which is the intent). Every year-end labelled (about 11 labels). Data: `capacity_timeline.csv` derived by Role A.
- Built-in check: the summed power at the retrieval date should land close to the `data_centers.csv` total. If it does not, the timeline stays out of the app.
- Caption must say that Epoch dates are estimates of when buildings became operational or are forecast to.

**Colour-blind and contrast evidence.** Validator results (dataviz skill) on 18 Oct: blue, vermillion, green and orange passed (worst adjacent deutan Delta-E 11.0); five colours passed; six passed (worst 9.6); adding yellow failed the lightness band. Contrast warnings on orange, sky and purple are cleared by direct labels and table views. Role B repeats the check in the browser (section 6, B).

### 3.4 Copy rules and claim hygiene (apply to `content.py`)
1. Two kinds of sentence: **Data** (numbers from facts) and **Our reading** (judgement, labelled as ours).
2. OWID = "data centres". Epoch = "tracked AI data centres". Never write "AI uses X% of electricity".
3. MW = "estimated facility power", never "consumption" or "draw" without "estimated".
4. Describe, do not cause: "rose", "is", not "drives", "causes", "crisis", "strain".
5. Every figure names its period; every comparison names its baseline ("share of that region's demand in that year").
6. One decimal for percentages, whole numbers for MW, one decimal for ratios, thousands separators.
7. Australian/British spelling: centre, colour.
8. `tests/test_copy.py` greps `content.py` for the banned stems (`caus`, `crisis`, `strain` outside the "cannot show" list, `will `, `AI uses`) and fails on a match.

### 3.5 Fact registry (`facts.py`, Role D)
`Fact(id, value, text, unit, source_file, how)`; `build_facts(dc_share, sites) -> dict[str, Fact]`. Ids: `latest_year`, `first_year`, `world_share_latest`, `world_share_first`, `us_share_latest`, `us_to_world_ratio`, `entity_share_latest`, `entity_share_first`, `entity_to_world_ratio` (these three take the lens entity), `n_sites`, `n_countries`, `n_sites_power`, `total_mw`, `largest_site_name`, `largest_site_mw`, `median_site_mw`, `top10_share_mw`, `n_sites_ge_large`, `large_site_mw` (constant 200), `us_share_of_mw`, `top4_owner_share_mw`. The footer expander **"Trace a number"** lists every fact with its text, source file and `how`; it is also the demo path for the recording's "trace a number" item.

## 4. Data package

### 4.1 Raw files (Role A downloads; commit byte-for-byte; never edit)
| File in `data/raw/` | URL | Licence to record |
|---|---|---|
| `epoch_data_centers.csv` | https://epoch.ai/data/data_centers/data_centers.csv | Creative Commons Attribution (confirm the version) |
| `owid_data_centers_share_electricity_demand.csv` | https://ourworldindata.org/grapher/data-centers-share-electricity-demand.csv?v=1&csvType=full&useColumnShortNames=true | OWID CC BY; IEA and Ember inputs keep their own terms (full metadata: https://api.ourworldindata.org/v1/indicators/1295514.metadata.json) |
| `epoch_data_center_timelines.csv` (SHOULD) | https://epoch.ai/data/data_centers/data_center_timelines.csv | as Epoch |

Record the retrieval date for each in `data/processed/meta.json`. **Freeze after Fri 6 Nov**: re-downloading later means re-running every test and re-reading every sentence.

### 4.2 Processed files (written by `scripts/make_processed.py`)
Write every CSV with `index=False` and `lineterminator="\n"`.

`dc_share.csv`: `entity` (text), `code` (text, may be empty), `year` (int), `share_pct` (float, percent). Transform: rename the long value column to `share_pct`; keep entity labels as in the source; add nothing, interpolate nothing.

`sites.csv`: `site` (`Name`), `owner` (`Owner` with the trailing `#...` tag removed and whitespace trimmed; blank becomes `Unattributed`), `owner_confidence` (the tag text without `#`, or empty), `country`, `power_mw` (`Current power (MW)`), `h100_equivalents`, `capex_usd_bn_2025`, `has_power` (`power_mw > 0`). Sites at 0 MW stay in the file; every chart states whether it includes them.

`capacity_timeline.csv` (SHOULD): `year_end` (date), `power_mw_total`, `is_forecast` (true when the date is after the retrieval date), `n_sites`.

`meta.json`: per source `url`, `licence`, `retrieved`, `source_updated`.

### 4.3 Data tests (Role A)
`tests/test_data_contract.py`: files exist; exact columns and dtypes; `share_pct` between 0 and 100; years are the expected set; `power_mw` is 0 or more; no `#` left in `owner`; `site` is unique; row counts equal the raw files. `tests/test_regeneration.py` plus a CI step that reruns the script and fails if `git status --porcelain data/processed` shows anything (this catches both changed and missing committed files).

### 4.4 Dictionary (Role A)
`docs/DATA_DICTIONARY.md` holds one section per raw and processed file with all eight fields the brief lists: source and URL, licence, columns and units, primary key, time coverage, latest observation, transform (plus retrieval date). `tests/test_dictionary.py` fails while any `TODO` remains.

### 4.5 Questions Role A must settle from the real files (record answers in the dictionary)
1. What does 0 MW mean for the 20 sites (planned, not yet operating, unknown)? Epoch's "Records" documentation decides.
2. Is `Current power (MW)` facility power, and as of what date?
3. Licence terms for the IEA and Ember inputs to the OWID file.
4. Whether OWID's 2025 value is an estimate, despite the "historical" column name.

## 5. Repository and engineering

### 5.1 Foundation PR (built first, branch `feature/foundation`)
1. `theme.py`: new tokens, `ENTITY_COLORS`, `apply_layout`; remove yellow and black from `CATEGORICAL`.
2. `.streamlit/config.toml` (light base, the tokens above, `gatherUsageStats = false`).
3. `.gitattributes`: `* text=auto eol=lf` and `data/raw/** -text` (stops the CRLF warnings and keeps raw files byte-exact).
4. `.github/workflows/ci.yml` (below).
5. Interface stubs only: `content.py`, `facts.py` (the `Fact` dataclass and function signatures), `charts/country.py`, `charts/owners.py`, `charts/timeline.py`; remove `charts/geo.py` and `charts/headline.py`.
6. `docs/BUILD_PLAN.md` (this plan) replaces `docs/TEAM_PLAN.md`; `README.md` carries the question, draft persona and stories.
7. `docs/evidence/` folder; updated first row of `docs/PROVENANCE.md`.
8. `pytest -q` must pass before the PR opens. Brendan merges it.

CI (`.github/workflows/ci.yml`):
```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.13", cache: pip, cache-dependency-path: requirements-dev.txt }
      - run: pip install -r requirements-dev.txt
      - run: python scripts/make_processed.py
      - run: test -z "$(git status --porcelain data/processed)"
      - run: pytest -q
```
Until Role A replaces it, the foundation's `scripts/make_processed.py` prints "not implemented yet" and exits 0, so CI is green on the first PRs.
(Action versions were not checked against current releases. Role B confirms the first run is green.)

### 5.2 Final layout
```
app.py  content.py  facts.py  theme.py                 D
charts/trend.py  charts/timeline.py                    B
charts/country.py                                      A
charts/owners.py  charts/sites.py                      C
scripts/make_processed.py                              A
data/raw/  data/processed/                             A
docs/BUILD_PLAN.md  DATA_DICTIONARY.md  PROVENANCE.md  DISCLOSURE.md  evidence/
tests/  .github/workflows/  .streamlit/config.toml
```

### 5.3 Git rules
- Branch `feature/<role>-<topic>`; PR titled "Role B: C1 trend chart"; one reviewer from a different role; CI green; squash merge; delete the branch.
- Commit as yourself. Nobody pushes work on someone else's behalf. Run `git pull --rebase origin main` before pushing.
- Only Role D edits `app.py`, `content.py`, `facts.py`, `theme.py`. Everyone appends (never reorders) rows in `docs/PROVENANCE.md`.
- After the foundation merge, nothing goes straight to `main`. Anything on `main` goes live on the deployed app.
- Review checklist: matches the chart card; tests added and green; caption fields present; no hand-typed number; provenance row added.

### 5.4 Deployment (Role A, Monday)
1. After Brendan agrees: `gh repo edit Bren3107/ai-datacentre-grid --visibility public --accept-visibility-change-consequences`.
2. share.streamlit.io, sign in with GitHub, create app: repo `Bren3107/ai-datacentre-grid`, branch `main`, file `app.py`, **Advanced settings: Python 3.13** (cannot be changed later without deleting and redeploying), URL slug `ai-datacentre-grid`.
3. Deploy the skeleton on Monday so platform problems show up early.
4. Measure load: Chrome DevTools, Network, disable cache, reload: Load under 5 s. Repeat after a wake-up. Save a screenshot to `docs/evidence/load-time.png`.
5. **Sleeping app.** Streamlit staff say apps sleep after 12 hours without visits and waking takes a button press and a wait. Scheduled empty commits and webhooks did not keep every app awake. Mitigation, in order: a manual visit by someone each day from 13 Nov and a visit on submission day; an optional scheduled headless-browser visit (GitHub Actions cron every 6 hours using Playwright to open the URL and click the wake-up button if present; efficacy unverified); if it keeps sleeping, a second copy on another host as Plan B.

### 5.5 Test inventory
| File | Owner | Checks |
|---|---|---|
| `test_smoke.py` (exists) | foundation | app renders without exception |
| `test_data_contract.py`, `test_regeneration.py`, `test_dictionary.py` | A | 4.3, 4.4 |
| `test_charts.py` | B | each builder: title, axis titles with units, one label per value, palette only, empty returns `None` |
| `test_app_interactions.py` | B | each lens value renders; region multiselect to empty shows the message; impossible filters show the message; each interaction run under 2 s |
| `test_facts.py` | C | recompute every fact with a *different* pandas expression and compare |
| `test_readme.py` | C | question string present; persona and decision present; three stories match the as-a/I-want/so-that pattern |
| `test_copy.py`, `test_lens_reading.py` | D | banned stems; each ratio branch |
| `test_provenance.py`, `test_disclosure.py` | D | four distinct people have rows; no `TODO` |

## 6. Role cards

Setup for everyone (needs Python 3.11 or newer; 3.13 is what we pin):
```bash
git clone https://github.com/Bren3107/ai-datacentre-grid.git
cd ai-datacentre-grid
python -m venv .venv
.venv\Scripts\activate        # PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
streamlit run app.py
```
Rough effort per role is 8 to 10 hours of build (rough estimate, with AI help), most of it by Tue 20 Oct.

### Role A: Data and delivery
Files: `scripts/make_processed.py`, `data/`, `docs/DATA_DICTIONARY.md`, `charts/country.py`, tests for data, deployment.
1. Download the two raw files (three if doing C5) into `data/raw/`; note the retrieval dates. Open each in a spreadsheet and look.
2. Answer the four questions in 4.5; write the answers in the dictionary.
3. Write `make_processed.py` to the schemas in 4.2. Run it twice and confirm the second run changes nothing.
4. Write `test_data_contract.py` and `test_regeneration.py`.
5. Open PR "Role A: data pipeline" by **Mon 12:00**. Others are waiting on it.
6. Build `charts/country.py` to card C3 (`build_figure(sites)` plus `render(sites)`).
7. Fill the dictionary; add `test_dictionary.py`.
8. Monday: flip public, deploy, measure load (5.4).
9. From 13 Nov: keep-alive visits; on 19 Nov tag `v1.0-submission` and run the fresh-clone check (section 9).

Done when: checks 5.1, 5.2, 5.3, 5.6, 4.1 and 3.x for C3 pass. Provenance example: "Claude drafted `make_processed.py`. Verified by recomputing total MW and each country's share with a separate pandas expression on the raw file, and by CI failing when regenerated files differ from the committed ones. It would have failed if the tag-stripping or the 0-MW rule were wrong."

### Role B: Trend and QA
Files: `charts/trend.py`, `charts/timeline.py` (SHOULD), `.github/workflows` first run, `tests/test_charts.py`, `tests/test_app_interactions.py`, `docs/evidence/`.
1. **Prototype C1 first (one hour).** Use fake rows with the real shape; confirm the 2 x 2 facets show every label without collisions. If not, use the fallback in the card.
2. Build `build_figure(dc_share, regions)` and `render(dc_share)` to card C1.
3. Swap to real data when Role A merges (Mon noon).
4. Write `test_charts.py` as a reusable contract (title, axis titles with units, labels, palette) that Roles A and C then call for their charts.
5. Write `test_app_interactions.py` (lens values, empty states, timing).
6. QA on the deployed URL (Tue): 1366x768 in DevTools device mode with no horizontal scrollbar; colour-blind emulation (DevTools, Rendering, Emulate vision deficiencies: protanopia, deuteranopia, tritanopia, achromatopsia); empty states; each story walked end to end. Save screenshots in `docs/evidence/`.
7. After 23 Oct: C5 if the timeline check passes.

Done when: 3.x for C1, 4.3, 4.4, 4.5 and 3.6 pass. Provenance example: "Claude drafted `trend.py`. Verified by reading the World 2025 label off the app and comparing with 1.5264845 in the raw CSV (rounds to 1.5), and by `test_charts.py` failing when a label is removed."

### Role C: Sites and facts verification
Files: `charts/owners.py`, `charts/sites.py`, `README.md`, `tests/test_facts.py`, `tests/test_readme.py`.
1. Build C2 to its card, then the Story 3 filter row (country, owner, minimum MW slider 0 to 900 step 50, include-0-MW checkbox), C4, and the largest-sites table.
2. Both filters and the empty state must respond in about a second (the data is under 100 rows, so use plain pandas filtering).
3. Write `test_facts.py` the day Role D's `facts.py` lands: for each fact, recompute it a different way and compare.
4. Finalise `README.md`: the question, persona with decision, three stories, and a **walk-through** line per story naming the control to use and the chart that changes.
5. Write `test_readme.py`.

Done when: 3.x for C2 and C4, 4.4, 1.1, 1.4, 1.5, 2.1 (verification half) pass. Provenance example: "Claude drafted `owners.py`. Verified by summing the raw file's Owner column with the tags stripped by hand for Google and comparing to the bar label. It would have failed if blank owners had been dropped."

### Role D: Story and shell
Files: `app.py`, `content.py`, `facts.py`, `theme.py`, `.streamlit/config.toml`, `docs/DISCLOSURE.md`, `docs/PROVENANCE.md` compile.
1. Mon morning: write `content.py` with every sentence from sections 1.4, 3.2 and 3.4, using placeholders.
2. Write `facts.py` (3.5) against the schemas, then run it on real data when Role A merges. Hand Role C the list of ids.
3. Build `app.py`: title, sub-line, Our answer, story links (`st.header(..., anchor="story-1")`), lens, the three story sections calling the chart modules, cannot-show and other-side blocks, footer reading `meta.json`, and the "Trace a number" expander.
4. Lens hero figure: a small `st.markdown` block, 3rem, weight 600, proportional figures, ink colour.
5. Write `test_copy.py` and `test_lens_reading.py`.
6. By Wed 21 Oct: read the whole page against section 3.4 with Role C.
7. Later: `DISCLOSURE.md`, `test_disclosure.py`, compile and check `PROVENANCE.md`.

Done when: 1.2, 1.3, 2.2, 2.3, 2.5, 4.2, 4.6, 5.4, 5.5 pass. Provenance example: "Claude drafted the lens copy. Verified by running `test_copy.py` (fails on banned stems) and by Role C's independent recomputation of every placeholder."

## 7. Calendar (today is Sun 18 Oct)

| When | What |
|---|---|
| Sun 18 | Approve plan; foundation PR merged; WhatsApp post; usernames collected; everyone clones and passes `pytest -q` and `streamlit run app.py`; A downloads data; D writes `content.py` |
| Mon 19 | A's data PR merged by 12:00 and repo public; B's CI first run green; A deploys skeleton by 17:00; B, C, D draft PRs by 18:00; group call to agree the verdict wording |
| Tue 20 | Reviews and merges by 14:00; integration; redeploy; B starts QA; fixes by 20:00. **MVP freeze 20:00**: all three stories work on the live URL |
| Wed 21 | QA fixes; rehearse; record (one retake allowed) |
| Thu 22 | Upload or link recordings and submit by 17:00 (a day early) |
| Fri 23 | Deadline 11:59pm |
| 24 Oct to 5 Nov | SHOULD items (C5, dictionary polish, copy review); write peer feedback |
| Fri 6 Nov | Peer feedback due. **Data freeze** |
| Mon 9 to Fri 13 Nov | Run the 30-check matrix; each person tests someone else's part. **Feature freeze Fri 13** |
| Mon 16 to Wed 18 Nov | Fixes only; tag `v1.0-rc` |
| Thu 19 Nov | Tag `v1.0-submission`; fresh-clone check; PDF built and submitted |
| Fri 20 Nov | Buffer; deadline 11:59pm |

Critical path: Role A's data PR on Monday. Everything else can start on fake rows of the real shape.

## 8. Marking-check matrix (30 checks: how built, how verified, evidence)

| # | Check | Built by | Verified by | Evidence |
|---|---|---|---|---|
| 1.1 | README states the question in one sentence | C | `test_readme.py` | test output |
| 1.2 | Question on the opening screen | D | `test_app_interactions.py` (first title) | test output |
| 1.3 | Question is arguable | D | "Other side" block present; reviewed Wed 21 | screenshot |
| 1.4 | README names persona and decision | C | `test_readme.py` | test output |
| 1.5 | Three user stories, as-a/I-want/so-that | C | `test_readme.py` regex | test output |
| 1.6 | Each story walkable in the app | B, C | README walk-through plus B's walk | screenshots |
| 2.1 | Every number traceable | D, A | `test_facts.py`, Trace-a-number expander | test output, screenshot |
| 2.2 | App states an answer in text | D | interaction test finds "Our answer" with no `{` left | test output |
| 2.3 | States what the data cannot show | D | interaction test finds the block with at least 4 bullets | test output |
| 2.4 | Units, baselines, time coverage stated | chart owners | `test_charts.py` caption fields | test output |
| 2.5 | Claims within the data | D, C | `test_copy.py` plus Wed 21 read | test output |
| 2.6 | Every chart titled or captioned | B | `test_charts.py` | test output |
| 3.1 | At least four charts | A, B, C | count of builders (and `at.get("plotly_chart")` if it works) | test output |
| 3.2 | At least three families | all | families table in README | README |
| 3.3 | Form matches task | chart owners | cards C1 to C4 reproduced in README | README |
| 3.4 | Axes and legends labelled with units | B | `test_charts.py` | test output |
| 3.5 | Values readable without hovering | chart owners | `test_charts.py` labels plus table twins | screenshots |
| 3.6 | Colours survive a CVD check | D, B | validator output plus DevTools emulation | `docs/evidence/` |
| 4.1 | Loads in under 5 s | A | DevTools measure, cold and warm | screenshot |
| 4.2 | Opens on something true about the whole dataset | D | interaction test: opening sub-line has `n_sites` | test output |
| 4.3 | Two or more interactions, about 1 s | B, C, D | lens, regions, filters; timing test | test output |
| 4.4 | Empty filter shows a message | B, C | interaction tests | test output |
| 4.5 | 1366x768, vertical scroll only | B | DevTools device mode | screenshot |
| 4.6 | Sources and last refresh on screen | D | interaction test reads footer date from `meta.json` | test output |
| 5.1 | Data folder with samples and processed files | A | `test_data_contract.py` | test output |
| 5.2 | Dictionary covers every dataset | A | `test_dictionary.py` | test output |
| 5.3 | Commit hash resolves and the app runs from it | A | fresh-clone check (section 9) | log in `docs/evidence/` |
| 5.4 | Provenance row from every member | D | `test_provenance.py`; read each verification cell | test output |
| 5.5 | Disclosure present | D | `test_disclosure.py` | test output |
| 5.6 | Processed files regenerate | A | CI reruns the script and checks `git status --porcelain data/processed` is empty | green CI run |

## 9. Recording kit (Part 1, due Fri 23 Oct)

Eight peer-checked items: within 5 minutes; audible and legible; question stated; persona named; own contribution on screen; a design decision with a named alternative; a displayed number traced to source; AI use disclosed with its check. Each missed item costs one of your 5 marks, and assessors stop at 5:00.

| Time | Say and show |
|---|---|
| 0:00 to 0:25 | The question and the persona with their decision (app top) |
| 0:25 to 1:10 | Your part live in the app, then your pull requests and commits on GitHub |
| 1:10 to 2:25 | One design decision you owned: the visual task, the form chosen, the alternative rejected, the specific reason (use your chart card, in your own words) |
| 2:25 to 3:40 | Trace one number: "Trace a number" expander, then the processed row, then the raw CSV cell, then the line in `make_processed.py` |
| 3:40 to 4:15 | AI use: tool, what you asked, what came back, the check that could have failed (read your provenance row) |
| 4:15 to 4:30 | Close |

Technique: screen and voice only; test audio first; browser zoom 125% so text is legible; close notifications; aim for 4:30. Record on Wed 21, retake once, upload a file or an unlisted link on Thu 22. After the deadline, watch each teammate's recording with the checklist and write two comments with rough times (what worked, what to change) by Fri 6 Nov.

**Final submission check (Thu 19 Nov, Role A):**
```bash
git clone https://github.com/Bren3107/ai-datacentre-grid.git fresh && cd fresh
git checkout v1.0-submission && git rev-parse HEAD
pip install -r requirements-dev.txt && python scripts/make_processed.py && test -z "$(git status --porcelain data/processed)" && pytest -q
streamlit run app.py
```
The PDF holds the app URL, the repo URL and that commit hash or tag.

## 10. Risks (pre-mortem: how we lose marks) and mitigations
1. **App asleep when marked** (4.1): daily visits from 13 Nov, optional scheduled visit, Plan B host.
2. **A label or colour a grader cannot read** (3.4 to 3.6): contract tests, validator and DevTools evidence, table twins.
3. **A number that cannot be traced** (2.1): `facts.py`, independent test, Trace-a-number expander.
4. **A claim past the data** (2.5): copy rules and the banned-stem test; "Our reading" always labelled.
5. **A role goes quiet:** another member may take over the work, but commits and provenance rows must say who did it. Raise it in the group within 24 hours of a missed milestone.
6. **Source data changes under us** (Epoch updates often): freeze after 6 Nov.
7. **Python drift on the host:** choose 3.13 at deploy; pins match local; relax pins only if the install fails.
8. **Merge collisions:** file ownership; only D edits `app.py`; rebase before pushing.
9. **Unverified assumptions in this plan:** see section 11.

## 11. What was checked and what was not
- **Run and confirmed (18 Oct):** Streamlit 1.63.0 provides `segmented_control`, `pills`, `plotly_chart(width=...)`, `header(anchor=...)`, `popover`, and the test harness supports segmented controls, multiselects and sliders; the scaffold's smoke test passes; the palette validator results and contrast ratios above; the OWID CSV read verbatim; OWID metadata (unit, definition, dates, sources).
- **Read through a web tool, not from the file:** the Epoch row list and every aggregate derived from it; the timelines columns; Epoch's coverage statement.
- **Not verified:** IEA and Ember licence terms; what 0 MW means; whether OWID 2025 is an estimate; Community Cloud's handling of Python 3.13 and of private repos; whether a headless visit keeps an app awake; whether 2 x 2 facets stay free of label collisions; whether the test harness can count Plotly elements; menu names in DevTools; all effort estimates; the GitHub Action versions.
- **Strongest objection to this plan:** it is heavy for four students in five days. Answer: the MVP for 23 Oct is only the lens, C1, C2, C3, C4 and filters on real data; tests, dictionary polish, C5 and evidence follow on the later dates, and every item is tagged to a date.

## Appendix: WhatsApp role cards (plain text)

```text
ROLE A - Data + delivery
You: download the 2 CSVs, write scripts/make_processed.py, data dictionary, country chart (C3), deploy on Streamlit Cloud, tag the final commit.
By Mon 12:00: data PR merged (everyone is waiting on it). Mon 17:00: skeleton app live.
Tests you write: data contract, regeneration, dictionary.

ROLE B - Trend + QA
You: line chart of data-centre share of electricity by region (C1) with a region picker, CI check, chart tests, then QA on the live app (1366x768, colour-blind, empty states, walk each story).
By Mon 18:00: C1 draft PR. Tue: QA.

ROLE C - Sites
You: owners ranking chart (C2), Story 3 filters + site-size chart (C4) + largest-sites table, README (persona + 3 stories + walk-through), tests that recompute the numbers a different way.
By Mon 18:00: draft PRs.

ROLE D - Story + shell
You: app.py page, all the wording (content.py), facts.py (every number comes from code), the scale lens, theme, disclosure, provenance table.
By Mon 15:00: facts.py and content.py PR.

Everyone: your own branch + PR, your own commits, one row in docs/PROVENANCE.md, your own 5-min recording. Plan: docs/BUILD_PLAN.md
```
