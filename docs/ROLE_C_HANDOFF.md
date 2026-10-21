# Role C hand-off (21 October 2026)

Author: yux7540-design. Branch: feature/role-c-sites-verification.

## Integration for Role D

Call `charts.owners.render(sites)` in Story 2 with the **unfiltered** processed sites table. Call `charts.sites.render(sites)` in Story 3; it owns its widget keys and filtering. Both chart builders preserve the original stub signatures and return None when empty. No changes to app.py, content.py, facts.py or theme.py are included.

The chart text is kept in these modules so the render functions work independently, matching Role A's country module. D can centralise these captions in content.py during integration.

## Corrections to the original plan

- Use **estimated IT power**, following Role A's data dictionary; facility power is a different measure.
- 100 MW bands extend dynamically beyond 999 MW: the current largest site is 1,037 MW. Zero-power sites have a separate bin when selected and never enter the positive-power bin.
- Empty country/owner selection means no matches. None in the pure filter function means unrestricted. The checkbox does not bypass a positive minimum threshold.
- Median and concentration calculations in the independent checks use sites above 0 MW. Top-four owners means named owners, excluding Unattributed; total tracked positive MW remains the denominator. Percentage values are on the 0–100 scale. D should confirm this convention before integrating.

## Pending cross-role work

- Role D's build_facts still raises NotImplementedError. The 18 registry comparisons are explicitly expected failures until that implementation arrives. They do not validate a missing implementation.
- Dynamic entity facts cannot yet be called through the current two-argument build_facts interface. Agree the entity-selection API with D, then add all-region comparisons.
- The main app remains the foundation scaffold until D wires in the modules; full-app QA and deployment are not verified by this branch.
- The live app URL must be added once A supplies it. IEA licence and 2025 status questions remain recorded in the dictionary.

## Validation

`python -m pytest -q`: 84 passed, 18 expected failures before browser QA.
`python scripts/make_processed.py`: processed files unchanged.

Independent chart checks aggregate the raw Epoch Owner column with the csv module, verify top-eight aggregation, test 99.9/100/999/1000/1100 MW boundaries, and exercise Streamlit checkbox, slider and empty-state behaviour. README checks validate the question, persona, decision, three stories, walkthroughs and chart families.

Browser QA: Chrome at 1366 x 768, no horizontal overflow (scroll width 1366). Both charts show all value labels. The include-zero checkbox updated the chart in 0.192 s in the final local measurement; this is not a deployed-app load benchmark. Screenshots and metrics are in docs/evidence/role-c-*. The distribution tick spacing was increased after visual review to prevent overlapping axis labels.
