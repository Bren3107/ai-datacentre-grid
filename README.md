# Is AI data-centre growth a grid problem, or still a small share of electricity demand?

Assignment 3, The Rise of Artificial Intelligence: Data Narrative Studio. An interactive data narrative built with Streamlit.

> Scaffold stage. Role D finalises the persona, user stories and run notes. See [docs/TEAM_PLAN.md](docs/TEAM_PLAN.md) for who owns what.

## The question

Is AI data-centre growth a grid problem, or still a small share of electricity demand?

## Persona and decision

TODO (Role D, agreed by the group): one named persona and the decision this app helps them make. A draft is in [docs/TEAM_PLAN.md](docs/TEAM_PLAN.md).

## User stories

TODO (Role D): three stories in "As a ..., I want ..., so that ..." form. Each one must be walkable in the app.

## Run it locally

```bash
pip install -r requirements.txt
python scripts/make_processed.py   # regenerates data/processed/ from data/raw/
streamlit run app.py
```

## Data

Source files are in `data/raw/`, files the app reads are in `data/processed/`, and every dataset is described in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

## AI provenance and disclosure

[docs/PROVENANCE.md](docs/PROVENANCE.md) lists every substantive AI use. [docs/DISCLOSURE.md](docs/DISCLOSURE.md) is the Data and AI disclosure statement.
