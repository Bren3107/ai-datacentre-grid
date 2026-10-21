"""Independent standard-library arithmetic for Role D's fact registry."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median
import pandas as pd
import pytest
from facts import build_facts

ROOT = Path(__file__).resolve().parents[1]

def expected_facts():
    with (ROOT / 'data/processed/sites.csv').open(encoding='utf-8-sig', newline='') as f:
        sites = list(csv.DictReader(f))
    with (ROOT / 'data/processed/dc_share.csv').open(encoding='utf-8-sig', newline='') as f:
        shares = list(csv.DictReader(f))
    first, last = min(int(r['year']) for r in shares), max(int(r['year']) for r in shares)
    def share(entity, year):
        return next(float(r['share_pct']) for r in shares if r['entity'] == entity and int(r['year']) == year)
    powered = [r for r in sites if float(r['power_mw']) > 0]
    ranked = sorted(powered, key=lambda r: float(r['power_mw']), reverse=True)
    total = sum(float(r['power_mw']) for r in powered)
    owners = defaultdict(float)
    for row in powered:
        if row['owner'] != 'Unattributed':
            owners[row['owner']] += float(row['power_mw'])
    return dict(first_year=first, latest_year=last,
        world_share_first=share('World', first), world_share_latest=share('World', last),
        us_share_latest=share('United States', last), us_to_world_ratio=share('United States', last) / share('World', last),
        n_sites=len(sites), n_countries=len({r['country'] for r in sites}), n_sites_power=len(powered),
        total_mw=total, largest_site_name=ranked[0]['site'], largest_site_mw=float(ranked[0]['power_mw']),
        median_site_mw=median(float(r['power_mw']) for r in powered),
        top10_share_mw=sum(float(r['power_mw']) for r in ranked[:10]) / total * 100,
        large_site_mw=200, n_sites_ge_large=sum(float(r['power_mw']) >= 200 for r in powered),
        us_share_of_mw=sum(float(r['power_mw']) for r in powered if r['country'] == 'United States') / total * 100,
        top4_owner_share_mw=sum(sorted(owners.values(), reverse=True)[:4]) / total * 100)

@pytest.fixture(scope='module')
def registry():
    try:
        return build_facts(pd.read_csv(ROOT / 'data/processed/dc_share.csv'), pd.read_csv(ROOT / 'data/processed/sites.csv'))
    except NotImplementedError:
        pytest.xfail('Role D build_facts is still a stub; independent verification is pending')

@pytest.mark.parametrize('fact_id', sorted(expected_facts()))
def test_fact_matches_independent_calculation(registry, fact_id):
    expected = expected_facts()[fact_id]
    assert fact_id in registry
    fact = registry[fact_id]
    assert fact.id == fact_id
    assert fact.text and fact.unit and fact.how and fact.source_file
    if fact_id != 'large_site_mw':
        assert (ROOT / fact.source_file).is_file()
    if isinstance(expected, str):
        assert fact.value == expected
    else:
        assert fact.value == pytest.approx(expected, rel=1e-9)
