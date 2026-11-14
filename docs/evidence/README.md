# Evidence

Screenshots and logs that back the marking checks. The matrix in [../BUILD_PLAN.md](../BUILD_PLAN.md) section 8 says which check each file supports.

| File | Supports | Who |
|---|---|---|
| `palette-validation.txt` | 3.6 colour-blind check | present (palette validator output, 18 Oct) |
| `cvd-*.png` | 3.6 | present (Role B, 31 Oct): the live app under deuteranopia, protanopia and tritanopia emulation; lines and bars stay distinguishable and carry value labels and legends |
| `load-time.txt` | 4.1 | present (Role A, 14 Nov, after main f1178a9): Load 3.4 to 3.7 s with an empty cache, five runs; four charts after 9.9 to 11.1 s. The tagged commit adds only this evidence, so the app code is the same |
| `load-time.png` | 4.1 | present (Brendan, 10 Nov 2026): Network tab in Brave (Chromium) DevTools on the deployed app, Disable cache ticked, window 1265 x 1080: DOMContentLoaded 1.46 s, Load 1.85 s. The Finish figure keeps growing because Streamlit keeps polling the server; BUILD_PLAN section 6 step 4 measures Load |
| `viewport-1366x768-*.png` | 4.5 | present (Role B, 31 Oct): four screenshots of the live app at 1366 x 768 (top, Stories 1, 2 and 3), no horizontal scrollbar |
| `empty-state-*.png` | 4.4 | present (Role B, 31 Oct): Regions, Countries and Owners cleared; each shows a message in place of the chart or an error |
| `fresh-clone.log` | 5.3 | present for main f1178a9 (Role A, 14 Nov): new clone and new venv; regeneration left `data/processed` unchanged, 189 tests passed, and the local app drew four charts with no exceptions. The `v1.0-submission` tag goes on the commit that adds this log, which changes only `docs/evidence` |
