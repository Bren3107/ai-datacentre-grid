# Is AI data-centre growth a grid problem, or still a small share of electricity demand?

Assignment 3, The Rise of Artificial Intelligence: Data Narrative Studio. An interactive data narrative built with Streamlit.

> Scaffold stage. The build plan is [docs/BUILD_PLAN.md](docs/BUILD_PLAN.md). Role C finalises this README with the group.

## The question

Is AI data-centre growth a grid problem, or still a small share of electricity demand?

## Persona and decision

DRAFT (Role C finalises with the group): Priya, a regional energy planner at a transmission or state energy agency. Decision: whether data-centre load deserves priority in grid planning now, or can be monitored for another planning cycle.

## User stories

DRAFT (Role C finalises with the group):

1. As a regional energy planner, I want to see how data centres' share of electricity demand has changed since 2020, so that I can tell whether the load is still marginal where I plan.
2. As a regional energy planner, I want to see which countries and owners hold the tracked AI data-centre capacity, so that I can judge how concentrated the new load is.
3. As a regional energy planner, I want to filter tracked sites by country, owner and size, so that I can see how much capacity sits in a few very large sites.

## Walk-through

TODO (Role C): one line per story naming the control to use and the chart that changes.

## Charts and Visual Vocabulary families

TODO (Role C, from the chart cards in the build plan): a table of chart, task, family and form.

## Run it locally

Needs Python 3.11 or newer (3.13 is what the requirements are pinned and tested on).

```bash
pip install -r requirements.txt
python scripts/make_processed.py   # regenerates data/processed/ from data/raw/
streamlit run app.py
```

## Data

Source files are in `data/raw/`, files the app reads are in `data/processed/`, and every dataset is described in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

## AI provenance and disclosure

[docs/PROVENANCE.md](docs/PROVENANCE.md) lists every substantive AI use. [docs/DISCLOSURE.md](docs/DISCLOSURE.md) is the Data and AI disclosure statement.
