"""Role A: open the deployed app in a headless browser so Streamlit Community Cloud keeps it awake.

Community Cloud puts an app to sleep after 12 hours without traffic, and waking it takes far longer
than the 5 s load-time check allows. .github/workflows/keep-awake.yml runs this every 3 hours.

    python scripts/keep_awake.py [--url URL] [--timeout SECONDS]

If the app is asleep it clicks the wake button. Either way it waits until all four charts are drawn,
prints how long that took, and exits 1 if they are not drawn within the timeout.
"""
import argparse
import sys
import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

URL = "https://ai-datacentre-grid-xjqdr9ehtm5vo4tdv2nxpb.streamlit.app/"
WAKE_BUTTON = "Yes, get this app back up!"
CHARTS = 4


def charts_drawn(page):
    """Most Plotly charts drawn in any one frame: Community Cloud serves the app inside an iframe."""
    most = 0
    for frame in page.frames:
        try:
            most = max(most, frame.locator(".js-plotly-plot").count())
        except PlaywrightError:  # a frame can detach while the app reloads
            pass
    return most


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=URL)
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1366, "height": 768})
        start = time.monotonic()
        woke = False
        drawn = 0
        try:
            # Community Cloud sometimes takes over 30 s (Playwright's default) to answer at all.
            page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout * 1000)
        except PlaywrightError as error:
            print(f"FAILED: could not open {args.url}: {error.message.splitlines()[0]}")
            sys.exit(1)
        while time.monotonic() - start < args.timeout:
            button = page.get_by_role("button", name=WAKE_BUTTON)
            if not woke and button.count() and button.first.is_visible():
                button.first.click()
                woke = True
                print("The app was asleep; clicked the wake button.")
            drawn = charts_drawn(page)
            if drawn >= CHARTS:
                break
            time.sleep(0.5)
        elapsed = time.monotonic() - start
        browser.close()

    state = "after waking it" if woke else "and it was already awake"
    if drawn < CHARTS:
        print(f"FAILED: {drawn} of {CHARTS} charts drawn after {elapsed:.1f} s ({args.url}).")
        sys.exit(1)
    print(f"{CHARTS} charts drawn {elapsed:.1f} s after opening {args.url}, {state}.")


if __name__ == "__main__":
    main()
