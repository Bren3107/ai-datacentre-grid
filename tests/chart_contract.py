"""Role B: the chart contract every builder in charts/ must pass (BUILD_PLAN 3.3 and 5.5).

Use it from any test file:

    from tests.chart_contract import assert_chart_ok, assert_empty_returns_none

    def test_owner_chart_meets_the_contract(sites):
        assert_chart_ok(owners.build_figure(sites))

    def test_owner_chart_empty():
        assert_empty_returns_none(owners.build_figure, sites.iloc[0:0])

The contract (marking checks 2.6, 3.4, 3.5 and the palette half of 3.6):
  1. the figure has a title
  2. every visible axis direction has a title; numeric axes name a unit in brackets,
     e.g. "Share of electricity demand (%)"; categorical or year axes are exempt
  3. every value can be read without hovering: each point has a text label, or the
     trace sits in the legend with its value in the name (as in C3 for small segments)
  4. every colour used comes from theme.py (plus white for text on dark fills)
  5. the builder returns None when there is nothing to draw
"""
import re

import plotly.graph_objects as go

import theme

UNITLESS_TITLES = {"Year", "Owner", "Region", "Country", "Site"}
EXTRA_ALLOWED = {"#FFFFFF"}  # label text on dark fills (C3's label_color)


def palette() -> set[str]:
    """Every hex colour defined in theme.py, so the contract follows the theme."""
    tokens = {v for v in vars(theme).values() if isinstance(v, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", v)}
    return {c.upper() for c in tokens | EXTRA_ALLOWED}


# ---- individual checks: each returns a list of problems -----------------------
def check_title(fig: go.Figure) -> list[str]:
    text = (fig.layout.title.text or "").strip()
    return [] if text else ["figure has no title"]


def _axes(fig: go.Figure, letter: str):
    layout = fig.to_plotly_json()["layout"]
    return [v for k, v in layout.items() if re.fullmatch(f"{letter}axis\\d*", k)] or [{}]


def check_axis_titles(fig: go.Figure) -> list[str]:
    problems = []
    for letter in ("x", "y"):
        visible = [a for a in _axes(fig, letter) if a.get("visible", True) is not False]
        if not visible:
            continue  # this direction is hidden on purpose (C3 hides its y-axis)
        titles = [(a.get("title") or {}).get("text") for a in visible]
        titles = [t.strip() for t in titles if t and t.strip()]
        if not titles:
            problems.append(f"no {letter}-axis title")
        for t in titles:
            if t not in UNITLESS_TITLES and not re.search(r"\(.+\)", t):
                problems.append(f"{letter}-axis title '{t}' has no unit in brackets")
    return problems


def _n_points(trace) -> int:
    values = trace.y if getattr(trace, "orientation", None) != "h" else trace.x
    return 0 if values is None else len(values)


def _is_data_trace(trace) -> bool:
    if trace.type == "bar":
        return True
    return trace.type == "scatter" and any(m in (trace.mode or "lines+markers") for m in ("markers", "lines"))


def check_labels(fig: go.Figure) -> list[str]:
    problems = []
    for i, trace in enumerate(fig.data):
        if not _is_data_trace(trace):
            continue
        n = _n_points(trace)
        texts = list(trace.text) if trace.text is not None and not isinstance(trace.text, str) else []
        labelled = len(texts) == n and all(str(t).strip() for t in texts)
        in_legend = trace.showlegend is not False and bool(re.search(r"\d", trace.name or ""))
        if not labelled and not in_legend:
            name = trace.name or f"trace {i}"
            problems.append(f"'{name}': {n} values but {sum(bool(str(t).strip()) for t in texts)} labels")
    return problems


def _colours(obj, found: set):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ("color", "fillcolor", "bgcolor", "paper_bgcolor", "plot_bgcolor", "bordercolor"):
                for v in value if isinstance(value, list) else [value]:
                    if isinstance(v, str) and v.startswith("#"):
                        found.add(v.upper())
            elif key != "template":  # the Plotly template's own defaults are overridden by theme.apply_layout
                _colours(value, found)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            _colours(item, found)


def check_palette(fig: go.Figure) -> list[str]:
    found: set = set()
    _colours(fig.to_plotly_json(), found)
    allowed = palette()
    return [f"colour {c} is not in theme.py" for c in sorted(found - allowed)]


# ---- public API ---------------------------------------------------------------
def chart_problems(fig: go.Figure) -> list[str]:
    return check_title(fig) + check_axis_titles(fig) + check_labels(fig) + check_palette(fig)


def assert_chart_ok(fig) -> None:
    assert fig is not None, "builder returned None for data that should draw a chart"
    problems = chart_problems(fig)
    assert not problems, "Chart contract failed:\n- " + "\n- ".join(problems)


def assert_empty_returns_none(builder, *args, **kwargs) -> None:
    result = builder(*args, **kwargs)
    assert result is None, f"{builder.__module__}.{builder.__name__} should return None when empty"
