# Role C hand-off (updated 26 October 2026)

Author: yux7540-design. Original implementation: feature/role-c-sites-verification. Follow-up: feature/role-c-final-verification.

## Integration for Role D

The main page now calls `charts.owners.render(sites)` in Story 2 with the **unfiltered** processed sites table and `charts.sites.render(sites)` in Story 3, which owns its widget keys and filtering. Both chart builders preserve the original stub signatures and return None when empty. No changes to app.py, content.py, facts.py or theme.py are included.

The chart text is kept in these modules so the render functions work independently, matching Role A's country module. D can centralise these captions in content.py during integration.

## Corrections to the original plan

- Use **estimated IT power**, following Role A's data dictionary; facility power is a different measure.
- 100 MW bands extend dynamically beyond 999 MW: the current largest site is 1,037 MW. Zero-power sites have a separate bin when selected and never enter the positive-power bin.
- Empty country/owner selection means no matches. None in the pure filter function means unrestricted. The checkbox does not bypass a positive minimum threshold.
- Median and concentration calculations in the independent checks use sites above 0 MW. Top-four owners means named owners, excluding Unattributed; total tracked positive MW remains the denominator. Percentage values are on the 0–100 scale. Role D's merged implementation uses this same convention.

## Current verification and remaining work

- Role D's `build_facts(dc_share, sites, entity=...)` is implemented. All 18 original independent registry checks now pass normally, and the obsolete NotImplementedError/expected-failure fallback has been removed.
- Formal tests now check three dynamic facts for each of the eight selectable regions (24 cases), including displayed rounding and provenance. An ID-coverage check fails if a new fact lacks an independent expectation.
- The Scale integration test now targets the actual segmented control. All three choices and eight country/region choices are exercised, including the hero figure and Trace a number row. Required widgets no longer silently skip tests.
- The minimum-size integration check compares the displayed largest-site rows with independently filtered CSV rows; it no longer relies on whether any chart exists elsewhere on the page.
- Update the README with the live app URL once A supplies it. Deployed load time, full-page 1366x768 screenshots and colour-vision checks remain for the A/B live QA pass.
- PR #8 contains the proposed disclosure/provenance update. Personal confirmation fields must be completed by the members themselves; this follow-up does not sign on anyone's behalf.
- IEA redistribution and the status of the 2025 value remain open as recorded in the dictionary.

## Validation history

The original 21 October branch had 84 passing tests and 18 expected failures while D's registry was absent. The integrated main branch on 26 October had 142 passing tests and one skipped Scale test. These historical results are superseded by the follow-up evidence in `docs/evidence/role-c-followup-tests.txt`.

Independent chart checks aggregate the raw Epoch Owner column with the csv module, verify top-eight aggregation, test 99.9/100/999/1000/1100 MW boundaries, and exercise Streamlit checkbox, slider and empty-state behaviour. README checks validate the question, persona, decision, three stories, walkthroughs and chart families.

Browser QA: Chrome at 1366 x 768, no horizontal overflow (scroll width 1366). Both charts show all value labels. The include-zero checkbox updated the chart in 0.192 s in the final local measurement; this is not a deployed-app load benchmark. Screenshots and metrics are in docs/evidence/role-c-*. The distribution tick spacing was increased after visual review to prevent overlapping axis labels.
