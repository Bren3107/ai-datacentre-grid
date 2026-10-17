# AI provenance matrix

One row per substantive AI use. Every member owns at least one row. The verification column must name a check that could have failed (a test, a hand recomputation, a comparison against the source), not "looked fine". Run `git pull` before editing and add your rows at the end.

| Artefact | Who | Tool | What was asked | What came back | How it was verified | Outcome |
|---|---|---|---|---|---|---|
| Repo scaffold: folder layout, `docs/` templates, `theme.py`, placeholder `app.py`, `tests/test_smoke.py`, `docs/TEAM_PLAN.md` (18 Oct 2026) | Brendan | Claude Code (Claude Sonnet 5.5) | Split the project into four roles for the chosen question, create the private repo, and set up starter files and templates | Role split, data contracts, templates and stubs. The contracts were drafted from a web read of the two source pages, not from the downloaded files | Ran `pytest tests/test_smoke.py` (the app must render without an exception; it fails on any syntax, import or render error): 1 passed. Imported every module and ran `apply_layout` on an empty figure: no error. Compared the versions in `requirements.txt` with the versions installed locally: they match. Not yet checked: the contract column names against the real CSV headers | Accepted as a scaffold. Data contracts stay provisional until Role A checks them against the downloaded files |
