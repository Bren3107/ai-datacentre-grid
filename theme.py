"""Shared colour tokens and figure layout so every chart looks like one app.

Colours were checked with the dataviz skill's palette validator (docs/evidence/palette-validation.txt).
Marks may use any token; text always uses INK, INK_2 or MUTED. Yellow and black are not used for data.
"""

PAPER = "#FCFCFB"
BAND = "#EEF3F8"
INK = "#14233A"
INK_2 = "#4B5A6E"
MUTED = "#5A6678"
GRID = "#D9DEE5"
CONTEXT_GREY = "#7D8796"

BLUE = "#0072B2"
VERMILLION = "#D55E00"
VERMILLION_TEXT = "#B04A00"  # use this, not VERMILLION, when the colour is text
GREEN = "#009E73"

# Reserved: below 3:1 against PAPER, so use only next to direct labels.
ORANGE = "#E69F00"
SKY = "#56B4E9"
PURPLE = "#CC79A7"

# Colour follows the entity everywhere in the app; every other entity is INK_2.
ENTITY_COLORS = {
    "World": BLUE,
    "United States": VERMILLION,
    "China": GREEN,
}
OTHER_ENTITY_COLOR = INK_2

CATEGORICAL = [BLUE, VERMILLION, GREEN, ORANGE, SKY, PURPLE]


def entity_color(name):
    """Fixed colour for a named entity, so filtering never repaints the survivors."""
    return ENTITY_COLORS.get(name, OTHER_ENTITY_COLOR)


def apply_layout(fig, title, x_title, y_title, height=420):
    """Title plus axis titles (put units in them) and margins that fit a 1366x768 screen."""
    fig.update_layout(
        title=dict(text=title, x=0, font=dict(color=INK, size=18)),
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        margin=dict(l=60, r=20, t=60, b=50),
        legend_title_text="",
        template="simple_white",
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(color=INK, size=13),
        transition_duration=0,
    )
    fig.update_xaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=INK_2))
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=INK_2))
    return fig
