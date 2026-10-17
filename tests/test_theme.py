import plotly.graph_objects as go

import theme


def test_categorical_palette_has_no_yellow_or_black():
    assert "#F0E442" not in theme.CATEGORICAL
    assert "#000000" not in theme.CATEGORICAL


def test_colour_follows_the_entity():
    assert theme.entity_color("World") == theme.BLUE
    assert theme.entity_color("United States") == theme.VERMILLION
    assert theme.entity_color("China") == theme.GREEN
    assert theme.entity_color("Africa (IEA)") == theme.OTHER_ENTITY_COLOR


def test_apply_layout_sets_titles_and_height():
    fig = theme.apply_layout(go.Figure(), "T", "X (unit)", "Y (unit)", height=300)
    assert fig.layout.title.text == "T"
    assert fig.layout.xaxis.title.text == "X (unit)"
    assert fig.layout.yaxis.title.text == "Y (unit)"
    assert fig.layout.height == 300
