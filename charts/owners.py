"""C2: whole-dataset ranking of estimated IT power by hardware owner."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import theme
from charts.country import _retrieved

OTHER = 'All other named owners'
UNATTRIBUTED = 'Unattributed'

def owner_totals(sites):
    powered = sites.loc[sites.power_mw > 0].copy()
    if powered.empty:
        return pd.DataFrame(columns=['owner', 'power_mw', 'share_pct'])
    powered['owner'] = powered.owner.fillna(UNATTRIBUTED).replace('', UNATTRIBUTED)
    totals = powered.groupby('owner', sort=True).power_mw.sum()
    named = totals.drop(UNATTRIBUTED, errors='ignore').sort_values(ascending=False, kind='stable')
    rows = list(named.iloc[:8].items()) + [(OTHER, named.iloc[8:].sum()), (UNATTRIBUTED, totals.get(UNATTRIBUTED, 0.0))]
    result = pd.DataFrame(rows, columns=['owner', 'power_mw'])
    result['share_pct'] = result.power_mw / powered.power_mw.sum() * 100
    return result

def build_figure(sites: pd.DataFrame):
    table = owner_totals(sites)
    if table.empty:
        return None
    labels = [f'{mw:,.0f} MW ({pct:.1f}%)' for mw, pct in zip(table.power_mw, table.share_pct)]
    fig = go.Figure(go.Bar(x=table.power_mw, y=table.owner, orientation='h', width=0.65,
        marker_color=[theme.CONTEXT_GREY if name in (OTHER, UNATTRIBUTED) else theme.BLUE for name in table.owner],
        text=labels, textposition='outside', textfont=dict(color=theme.INK, size=12), cliponaxis=False, hoverinfo='skip'))
    theme.apply_layout(fig, 'Tracked AI data-centre IT power by owner', 'Estimated IT power (MW)', 'Owner')
    fig.update_layout(showlegend=False, margin=dict(l=170, r=135, t=60, b=55))
    fig.update_yaxes(autorange='reversed', fixedrange=True)
    fig.update_xaxes(range=[0, table.power_mw.max() * 1.12], fixedrange=True, tickformat=',.0f')
    return fig

def render(sites: pd.DataFrame) -> None:
    chart, notes = st.columns([8, 4])
    with chart:
        fig = build_figure(sites)
        if fig is None:
            st.info('No tracked sites with power above 0 MW to show.')
        else:
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
            with st.expander('Show the numbers'):
                st.dataframe(owner_totals(sites).rename(columns={'owner': 'Owner', 'power_mw': 'Estimated IT power (MW)', 'share_pct': 'Share (%)'}).round(1), hide_index=True, width='stretch')
    with notes:
        st.markdown(
            '**What it shows:** estimated IT power of tracked AI data centres summed by listed owner across the whole dataset. '
            'Only sites above 0 MW are included; blank owners are shown as Unattributed. '
            'Owner means the AI hardware owner, not necessarily the facility operator.  \n'
            '**Unit:** megawatts (MW); shares use all tracked IT power above 0 MW, including Unattributed. IT power excludes cooling and other facility overhead.  \n'
            f'**Period:** snapshot retrieved {_retrieved()}.  \n'
            '**Source:** Epoch AI, AI data centers (CC BY 4.0).')
