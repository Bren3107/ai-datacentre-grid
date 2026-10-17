"""Shared colours and figure layout so every chart looks like one app."""

# Okabe-Ito palette, chosen to stay distinguishable under common colour vision deficiencies.
PALETTE = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
    "black": "#000000",
}

CATEGORICAL = [
    PALETTE[name]
    for name in ("blue", "orange", "green", "vermillion", "sky_blue", "purple", "yellow", "black")
]


def apply_layout(fig, title, x_title, y_title, height=420):
    """Title plus axis titles (put units in them) and margins that fit a 1366x768 screen."""
    fig.update_layout(
        title=dict(text=title, x=0),
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        margin=dict(l=60, r=20, t=60, b=50),
        legend_title_text="",
        template="simple_white",
    )
    return fig
