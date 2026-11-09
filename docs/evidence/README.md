# Evidence

Screenshots and logs that back the marking checks. The matrix in [../BUILD_PLAN.md](../BUILD_PLAN.md) section 8 says which check each file supports.

| File | Supports | Who |
|---|---|---|
| `palette-validation.txt` | 3.6 colour-blind check | present (palette validator output, 18 Oct) |
| `cvd-*.png` | 3.6 | Role B: DevTools vision-deficiency emulation of the live app |
| `load-time.txt` | 4.1 | present (Role A, 31 Oct): Load 3.1 to 4.0 s with an empty cache, five runs; four charts after 9.4 to 10.5 s. Re-run `scripts/measure_load.py` on the submitted commit |
| `viewport-1366x768-*.png` | 4.5 | Role B: no horizontal scrollbar |
| `empty-state-*.png` | 4.4 | Role B / C |
| `fresh-clone.log` | 5.3 | present for main 3f2413d (Role A, 31 Oct). Re-run on `v1.0-submission` before submitting, with the commands in BUILD_PLAN section 9 |
