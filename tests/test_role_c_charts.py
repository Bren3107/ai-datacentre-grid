"""Role C chart arithmetic, boundary and interaction regression tests."""
import csv
from collections import defaultdict
from pathlib import Path
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from charts import owners, sites
import theme

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def data():
    return pd.read_csv(ROOT / 'data/processed/sites.csv')

def test_owner_totals_against_raw_csv(data):
    expected = defaultdict(float)
    with (ROOT / 'data/raw/epoch_data_centers.csv').open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            owner = row['Owner'].split('#')[0].strip() or 'Unattributed'
            expected[owner] += float(row['Current power (MW)'] or 0)
    result = owners.owner_totals(data)
    total = sum(expected.values())
    for row in result.itertuples():
        if row.owner != owners.OTHER:
            assert row.power_mw == pytest.approx(expected[row.owner])
        assert row.share_pct == pytest.approx(row.power_mw / total * 100)
    assert result.power_mw.sum() == pytest.approx(total)
    assert result.share_pct.sum() == pytest.approx(100)
    assert result.owner.iloc[-2:].tolist() == [owners.OTHER, owners.UNATTRIBUTED]
    assert result.power_mw.iloc[:-2].is_monotonic_decreasing

def test_top_eight_and_catchalls():
    frame = pd.DataFrame({'owner': [f'Owner {i}' for i in range(10)] + ['Unattributed'], 'power_mw': list(range(1, 11)) + [5]})
    result = owners.owner_totals(frame)
    assert len(result) == 10
    assert result.iloc[-2].power_mw == 3
    assert result.iloc[-1].power_mw == 5

def test_boundaries_zero_and_overflow():
    frame = pd.DataFrame({'power_mw': [0, 0.1, 99.9, 100, 199.99, 200, 999, 1000, 1037, 1100]})
    result = sites.size_counts(frame).set_index('band')['count']
    assert result.sum() == len(frame)
    assert result['0 MW'] == 1
    assert result['0–99'] == 2
    assert result['100–199'] == 2
    assert result['1000–1099'] == 2
    assert result['1100–1199'] == 1

def test_filters_and_largest(data):
    chosen = sites.filter_sites(data, ['United States'], ['Google'], 200, True)
    expected = [r.site for r in data.itertuples() if r.country == 'United States' and r.owner == 'Google' and r.power_mw >= 200]
    assert chosen.site.tolist() == expected
    assert sites.filter_sites(data, [], None, 0, True).empty
    assert sites.filter_sites(data, None, [], 0, True).empty
    assert not sites.filter_sites(data, None, None, 0, False).power_mw.eq(0).any()
    assert len(sites.filter_sites(data, None, None, 0, True)) == len(data)
    assert not sites.filter_sites(data, None, None, 50, True).power_mw.eq(0).any()
    biggest = sites.largest_sites(data)
    assert len(biggest) == 10 and biggest.power_mw.is_monotonic_decreasing
    assert biggest.power_mw.iloc[0] == data.power_mw.max()

@pytest.mark.parametrize('module', [owners, sites])
def test_chart_contract(data, module):
    fig = module.build_figure(data)
    assert fig.layout.title.text
    assert '(MW)' in fig.layout.xaxis.title.text
    assert fig.layout.yaxis.title.text
    assert fig.layout.transition.duration == 0
    trace = fig.data[0]
    assert len(trace.text) == len(trace.x)
    assert trace.textposition == 'outside'
    colours = [trace.marker.color] if isinstance(trace.marker.color, str) else trace.marker.color
    assert set(colours) <= {theme.BLUE, theme.CONTEXT_GREY}
    assert module.build_figure(data.iloc[:0]) is None

def test_render_filters_and_empty_states():
    script = "from pathlib import Path\nimport pandas as pd\nfrom charts.sites import render\nrender(pd.read_csv(" + repr(str(ROOT / 'data/processed/sites.csv')) + "))"
    at = AppTest.from_string(script).run(timeout=20)
    assert not at.exception
    assert len(at.dataframe) == 2
    at.checkbox[0].check().run()
    assert not at.exception
    assert at.dataframe[0].value['Number of sites'].sum() == len(pd.read_csv(ROOT / 'data/processed/sites.csv'))
    at.slider[0].set_value(900).run()
    assert not at.exception
    assert at.dataframe[1].value['Estimated IT power (MW)'].min() >= 900
    at.multiselect[0].set_value([]).run()
    assert not at.exception
    assert at.info[0].value == sites.EMPTY_MESSAGE
    assert len(at.dataframe) == 0
