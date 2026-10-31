"""Role A: measure how long the deployed app takes to load (check 4.1, under 5 s).

    python scripts/measure_load.py [--url URL] [--cold 5] [--warm 3]

Each cold run uses a new browser profile, so nothing is cached: the same as DevTools with
"Disable cache" ticked. Warm runs revisit in the same profile. For every run it prints:

  DOMContentLoaded, Load  the page's own navigation timing, the two figures DevTools shows in the
                          Network status bar (BUILD_PLAN 6 step 4 measures Load)
  question, 4 charts      seconds from starting the visit until the question heading, then all
                          four charts, are drawn inside the app

If the app is asleep it says so, clicks the wake button and leaves that run out of the summary.
"""
import argparse
import statistics
import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from keep_awake import CHARTS, URL, WAKE_BUTTON, charts_drawn


def heading_drawn(page):
    for frame in page.frames:
        try:
            if frame.locator("h1", has_text="grid problem").count():
                return True
        except PlaywrightError:
            pass
    return False


def visit(context, url, timeout):
    page = context.new_page()
    start = time.monotonic()
    page.goto(url, wait_until="load", timeout=timeout * 1000)
    nav = page.evaluate("performance.getEntriesByType('navigation')[0].toJSON()")
    row = {"DOMContentLoaded": nav["domContentLoadedEventEnd"] / 1000, "Load": nav["loadEventEnd"] / 1000}
    asleep = False
    while time.monotonic() - start < timeout:
        button = page.get_by_role("button", name=WAKE_BUTTON)
        if not asleep and button.count() and button.first.is_visible():
            button.first.click()
            asleep = True
        if "question" not in row and heading_drawn(page):
            row["question"] = time.monotonic() - start
        if charts_drawn(page) >= CHARTS:
            row["4 charts"] = time.monotonic() - start
            break
        time.sleep(0.2)
    page.close()
    return row, asleep


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=URL)
    parser.add_argument("--cold", type=int, default=5)
    parser.add_argument("--warm", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()

    columns = ["DOMContentLoaded", "Load", "question", "4 charts"]
    results = {"cold": [], "warm": []}
    print(f"{args.url}  viewport 1366x768, headless Chromium, times in seconds")
    print(f"{'run':<8}" + "".join(f"{c:>18}" for c in columns))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for kind, runs in (("cold", args.cold), ("warm", args.warm)):
            context = None
            for i in range(runs):
                if kind == "cold" or context is None:
                    if context:
                        context.close()
                    context = browser.new_context(viewport={"width": 1366, "height": 768})
                    if kind == "warm":
                        visit(context, args.url, args.timeout)  # fills the cache; not counted
                row, asleep = visit(context, args.url, args.timeout)
                cells = "".join(f"{row[c]:>18.1f}" if c in row else f"{'not drawn':>18}" for c in columns)
                print(f"{kind} {i + 1:<3}" + cells + ("   app was asleep; woken, not counted" if asleep else ""))
                if not asleep:
                    results[kind].append(row)
            context.close()
        browser.close()

    print()
    for kind, rows in results.items():
        for c in columns:
            values = [r[c] for r in rows if c in r]
            if values:
                print(f"{kind} {c}: median {statistics.median(values):.1f}, "
                      f"range {min(values):.1f} to {max(values):.1f} ({len(values)} runs)")


if __name__ == "__main__":
    main()
