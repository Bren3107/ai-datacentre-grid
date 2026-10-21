"""Story 3: filters, exhaustive 100 MW bands and largest selected sites."""
import math
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import theme
from charts.country import _retrieved

EMPTY_MESSAGE = 'No tracked sites match these filters. Lower the minimum size, add a country or owner, or clear the filters.'

def filter_sites(sites: pd.DataFrame, countries, owners, min_mw, include_zero) -> pd.DataFrame:
    """None means unrestricted; an empty list means no matching sites."""
    mask = sites.power_mw.ge(min_mw)
    if not include_zero:
        mask &= sites.power_mw.gt(0)
    if countries is not None:
        mask &= sites.country.isin(countries)
    if owners is not None:
        mask &= sites.owner.isin(owners)
    return sites.loc[mask].copy()

def size_counts(filtered):
    if filtered.empty:
        return pd.DataFrame(columns=['band', 'count'])
    positive = filtered.loc[filtered.power_mw > 0, 'power_mw']
    upper = max(1000, (math.floor(float(positive.max()) / 100) + 1) * 100) if len(positive) else 1000
    edges = list(range(0, upper + 1, 100))
    labels = [f'{lo}\u2013{lo + 99}' for lo in edges[:-1]]
    counts = pd.cut(positive, bins=edges, labels=labels, right=False).value_counts(sort=False).reindex(labels, fill_value=0)
    rows = list(zip(labels, counts.astype(int)))
    zeros = int(filtered.power_mw.eq(0).sum())
    if zeros:
        rows.insert(0, ('0 MW', zeros))
    return pd.DataFrame(rows, columns=['band', 'count'])

def build_figure(filtered: pd.DataFrame):
    table = size_counts(filtered)
    if table.empty:
        return None
    fig = go.Figure(go.Bar(x=table.band, y=table['count'], text=table['count'].astype(str),
        textposition='outside', textfont=dict(color=theme.INK), marker_color=theme.BLUE, cliponaxis=False, hoverinfo='skip'))
    theme.apply_layout(fig, 'How big are the tracked AI sites?', 'Estimated IT power per site (MW)', 'Number of sites')
    fig.update_layout(showlegend=False, margin=dict(l=55, r=20, t=60, b=100))
    fig.update_xaxes(type='category', tickangle=-45, fixedrange=True)
    fig.update_yaxes(range=[0, max(1, table['count'].max()) * 1.22], dtick=max(1, math.ceil(table['count'].max() / 6)), fixedrange=True)
    return fig

def largest_sites(filtered):
    return filtered.sort_values(['power_mw', 'site'], ascending=[False, True]).head(10)[['site', 'owner', 'country', 'power_mw']].copy()

def render(sites: pd.DataFrame) -> None:
    countries = sorted(sites.country.dropna().unique())
    owners = sorted(sites.owner.dropna().unique())
    controls = st.columns([3, 3, 2, 2])
    with controls[0]:
        chosen_countries = st.multiselect('Countries', countries, default=countries, key='sites_countries')
    with controls[1]:
        chosen_owners = st.multiselect('Owners', owners, default=owners, key='sites_owners')
    with controls[2]:
        minimum = st.slider('Minimum IT power (MW)', 0, 900, 0, 50, key='sites_min_mw')
    with controls[3]:
        include_zero = st.checkbox('Include sites reporting 0 MW', value=False, key='sites_include_zero')
    st.caption('All countries and owners are selected initially. Clear a picker to select none; select all entries to restore the full selection. The minimum still applies when 0 MW sites are included.')
    selected = filter_sites(sites, chosen_countries, chosen_owners, minimum, include_zero)
    if selected.empty:
        st.info(EMPTY_MESSAGE)
        return
    chart, notes = st.columns([8, 4])
    with chart:
        st.plotly_chart(build_figure(selected), width='stretch', config={'displayModeBar': False})
        with st.expander('Show the numbers'):
            st.dataframe(size_counts(selected).rename(columns={'band': 'IT power band (MW)', 'count': 'Number of sites'}), hide_index=True, width='stretch')
    with notes:
        st.markdown(
            '**What it shows:** selected tracked AI data centres in each 100 MW band. '
            'Each band includes its lower boundary and excludes the next boundary; labels abbreviate continuous intervals (99.9 belongs to 0\u201399). '
            'Selected zero-power sites appear separately and are never counted twice. Bands extend beyond 999 MW when needed.  \n'
            '**Unit:** site counts by estimated IT power (MW), excluding cooling and other facility overhead.  \n'
            f'**Period:** snapshot retrieved {_retrieved()}.  \n'
            '**Source:** Epoch AI, AI data centers (CC BY 4.0).')
    st.subheader('Largest sites in this selection')
    st.dataframe(largest_sites(selected).rename(columns={'site': 'Site', 'owner': 'Owner', 'country': 'Country', 'power_mw': 'Estimated IT power (MW)'}), hide_index=True, width='stretch')
