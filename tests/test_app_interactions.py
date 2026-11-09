"""Role B: interaction tests (BUILD_PLAN 5.5; marking checks 1.2, 4.3, 4.4).

Each interaction must respond in under 2 s (the brief asks for about a second; 2 s is our
ceiling inside a test runner). Integrated controls are required: missing widgets now fail
rather than silently skipping. Scale uses Streamlit segmented_control.
"""
import time
import csv
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


@pytest.mark.parametrize('option, label', [
    ('World', 'of world electricity demand went to data centres'),
    ('Country or region', 'of electricity demand in United States'),
    ('Site', 'estimated IT power of the largest tracked AI data centre'),
])
def test_each_scale_option_renders_fast(app, option, label):
    selector = app.segmented_control(key='scale')
    assert selector.options == ['World', 'Country or region', 'Site']
    selector.set_value(option)
    elapsed = timed_run(app)
    assert not app.exception, f"Scale '{option}' raised"
    assert app.segmented_control(key='scale').value == option
    hero = [m.value for m in app.markdown if 'font-size:3rem' in m.value]
    assert len(hero) == 1 and label in hero[0]
    assert bool(list(app.selectbox)) == (option == 'Country or region')
    assert elapsed < LIMIT_S, f"Scale '{option}' took {elapsed:.2f} s"


with (ROOT / 'data/processed/dc_share.csv').open(encoding='utf-8-sig', newline='') as handle:
    SHARE_ROWS = list(csv.DictReader(handle))
LAST_YEAR = max(int(row['year']) for row in SHARE_ROWS)
REGION_SHARES = {
    row['entity']: float(row['share_pct']) for row in SHARE_ROWS
    if int(row['year']) == LAST_YEAR and row['entity'] not in ('World', 'World excl. United States and China')
}


@pytest.mark.parametrize('region', sorted(REGION_SHARES))
def test_region_picker_updates_the_lens_and_trace(app, region):
    app.segmented_control(key='scale').set_value('Country or region').run()
    assert not app.exception
    picker = app.selectbox(key='lens_entity')
    assert set(picker.options) == set(REGION_SHARES)
    picker.set_value(region)
    elapsed = timed_run(app)
    assert not app.exception
    hero = next(m.value for m in app.markdown if 'font-size:3rem' in m.value)
    assert f'{REGION_SHARES[region]:.1f}%' in hero
    assert f'of electricity demand in {region}' in hero
    trace = next(frame.value for frame in app.dataframe if 'Id' in frame.value.columns)
    row = trace.set_index('Id').loc['entity_share_latest']
    assert float(row['Exact value']) == pytest.approx(REGION_SHARES[region])
    assert region in row['How it is calculated']
    assert elapsed < LIMIT_S, f'{region} took {elapsed:.2f} s'


def test_trend_empty_state_inside_the_app(app):
    picker = _widget(app, "multiselect", "trend_regions")
    assert picker is not None, "Story 1 region picker must be integrated"
    picker.set_value([])
    elapsed = timed_run(app)
    assert trend.EMPTY_MESSAGE in infos(app)
    assert elapsed < LIMIT_S


def test_site_filters_that_match_nothing_show_the_message(app):
    countries = _widget(app, "multiselect", "sites_countries")
    assert countries is not None, "Story 3 country picker must be integrated"
    countries.set_value([])
    elapsed = timed_run(app)
    assert not app.exception
    assert any(SITES_EMPTY in m for m in infos(app))
    assert elapsed < LIMIT_S


def test_site_minimum_size_filters_the_largest_sites_table(app):
    slider = _widget(app, 'slider', 'sites_min_mw')
    assert slider is not None, 'Story 3 size slider must be integrated'
    slider.set_value(900)
    _widget(app, 'checkbox', 'sites_include_zero').uncheck()
    elapsed = timed_run(app)
    assert not app.exception
    assert elapsed < LIMIT_S
    with (ROOT / 'data/processed/sites.csv').open(encoding='utf-8-sig', newline='') as handle:
        expected = [row for row in csv.DictReader(handle) if float(row['power_mw']) >= 900]
    expected.sort(key=lambda row: (-float(row['power_mw']), row['site']))
    tables = [frame.value for frame in app.dataframe if 'Site' in frame.value.columns]
    if expected:
        assert len(tables) == 1
        assert tables[0]['Site'].tolist() == [row['site'] for row in expected[:10]]
        assert tables[0]['Estimated IT power (MW)'].tolist() == [float(row['power_mw']) for row in expected[:10]]
    else:
        assert not tables
        assert any(SITES_EMPTY in message for message in infos(app))
