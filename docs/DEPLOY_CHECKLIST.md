# Deploy checklist (Role A, BUILD_PLAN section 5.4)

Brendan clicks through this; nothing here has been done for him. The repo `Bren3107/ai-datacentre-grid` is already public (checked with `gh repo view` on 20 Oct 2026), so step 1 of 5.4 is done.

## Before deploying

- [ ] PR "Role A: data pipeline" merged to `main` (squash), CI green on `main`.
- [ ] On `main`: `pytest -q` passes and `streamlit run app.py` opens locally.

## Create the app (share.streamlit.io)

- [ ] Sign in with GitHub as Bren3107.
- [ ] Create app, "Deploy a public app from GitHub". Repository `Bren3107/ai-datacentre-grid`, branch `main`, main file `app.py`.
- [ ] App URL slug: `ai-datacentre-grid`.
- [ ] **Advanced settings, Python version 3.13.** This cannot be changed later without deleting and redeploying.
- [ ] Deploy. Wait for "Your app is in the oven" to finish; read the log for install errors (`requirements.txt` pins streamlit 1.63.0, plotly 6.3.1, pandas 3.0.5).
- [ ] Open the URL in a private window (not signed in) and confirm it loads without a login page. The solo repo's app redirected to a login because its repo was private; this one should not.
- [ ] Paste the URL into the group chat and into `README.md` (Role C owns the README; send it to Ming).

## Measure load time (check 4.1, target under 5 s)

- [ ] Chrome, open the app URL, DevTools (F12), Network tab, tick "Disable cache".
- [ ] Reload. Read "Load" in the bottom status bar once the charts have drawn. Note "DOMContentLoaded" and "Load".
- [ ] Screenshot the Network panel with the status bar visible; save as `docs/evidence/load-time.png`.
- [ ] Repeat after the app has slept (next morning, press the wake-up button, then reload with cache disabled); save as `docs/evidence/load-time-after-wake.png`.
- [ ] If Load is over 5 s, tell the group; the solo build measured 8.9 s locally, so this is a live risk.

## After deploying

- [ ] Every merge to `main` redeploys. Check the live app after each merge.
- [ ] From 13 Nov: open the app once a day so it does not sleep (BUILD_PLAN 5.4 step 5).
