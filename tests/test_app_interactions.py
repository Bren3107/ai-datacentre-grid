"""Role B: interaction tests (BUILD_PLAN 5.5; marking checks 1.2, 4.3, 4.4).

Each interaction must respond in under 2 s (the brief asks for about a second; 2 s is our
ceiling inside a test runner). Tests for parts other roles have not merged yet skip with a
reason instead of failing, and start running as soon as the widget appears in app.py.
"""
import time
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from charts import trend
from content import QUESTION

ROOT = Path(__file__).resolve().parents[1]
APP = str(ROOT / "app.py")
LIMIT_S = 2.0
SITES_EMPTY = "No tracked sites match these filters"

TREND_PAGE = f"""
import sys
sys.path.insert(0, {str(ROOT)!r})
import pandas as pd
from charts import trend
trend.render(pd.read_csv({str(ROOT / "data" / "processed" / "dc_share.csv")!r}))
"""


def timed_run(at):
    start = time.perf_counter()
    at.run()
    return time.perf_counter() - start


def infos(at):
    return [i.value for i in at.info]


# ---- C1 region picker (Role B) ----------------------------------------------
@pytest.fixture
def trend_page():
    at = AppTest.from_string(TREND_PAGE, default_timeout=30)
    at.run()
    assert not at.exception
    return at


def test_trend_opens_with_the_four_default_regions(trend_page):
    assert trend_page.multiselect(key="trend_regions").value == trend.DEFAULT_REGIONS
    assert trend.EMPTY_MESSAGE not in infos(trend_page)


def test_trend_empty_picker_shows_the_message_fast(trend_page):
    trend_page.multiselect(key="trend_regions").set_value([])
    elapsed = timed_run(trend_page)
    assert not trend_page.exception
    assert trend.EMPTY_MESSAGE in infos(trend_page)
    assert elapsed < LIMIT_S, f"took {elapsed:.2f} s"


def test_trend_changing_regions_redraws_fast(trend_page):
    trend_page.multiselect(key="trend_regions").set_value(["World", "North America (IEA)"])
    elapsed = timed_run(trend_page)
    assert not trend_page.exception
    assert trend.EMPTY_MESSAGE not in infos(trend_page)
    assert elapsed < LIMIT_S, f"took {elapsed:.2f} s"


# ---- the whole app ----------------------------------------------------------
@pytest.fixture
def app():
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    assert not at.exception
    return at


def test_question_is_the_first_title(app):
    assert app.title[0].value == QUESTION


def _widget(at, kind, key):
    try:
        return getattr(at, kind)(key=key)
    except KeyError:
        return None


def _scale_selector(at):
    for kind in ("radio", "selectbox"):
        for w in getattr(at, kind):
            if "scale" in (w.label or "").lower() or "lens" in (w.key or "").lower():
                return w
    return None


def test_each_scale_option_renders_fast(app):
    scale = _scale_selector(app)
    if scale is None:
        pytest.skip("waiting for Role D's Scale selector in app.py")
    for option in scale.options:
        _scale_selector(app).set_value(option)
        elapsed = timed_run(app)
        assert not app.exception, f"Scale '{option}' raised"
        assert elapsed < LIMIT_S, f"Scale '{option}' took {elapsed:.2f} s"


def test_trend_empty_state_inside_the_app(app):
    picker = _widget(app, "multiselect", "trend_regions")
    if picker is None:
        pytest.skip("waiting for Role D to call trend.render in app.py")
    picker.set_value([])
    elapsed = timed_run(app)
    assert trend.EMPTY_MESSAGE in infos(app)
    assert elapsed < LIMIT_S


def test_site_filters_that_match_nothing_show_the_message(app):
    countries = _widget(app, "multiselect", "sites_countries")
    if countries is None:
        pytest.skip("waiting for Role C's site filters in app.py")
    countries.set_value([])
    elapsed = timed_run(app)
    assert not app.exception
    assert any(SITES_EMPTY in m for m in infos(app))
    assert elapsed < LIMIT_S


def test_site_minimum_size_above_every_site_shows_the_message(app):
    slider = _widget(app, "slider", "sites_min_mw")
    if slider is None:
        pytest.skip("waiting for Role C's site filters in app.py")
    slider.set_value(900)
    _widget(app, "checkbox", "sites_include_zero").uncheck()
    elapsed = timed_run(app)
    assert not app.exception
    assert elapsed < LIMIT_S
    # 900 MW may still match a site; the message must appear exactly when nothing matches
    if not app.get("plotly_chart"):
        assert any(SITES_EMPTY in m for m in infos(app))
