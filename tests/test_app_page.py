"""Role D: the opening screen, checked through Streamlit's test harness."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

import content

APP = Path(__file__).resolve().parents[1] / "app.py"


def _run():
    return AppTest.from_file(str(APP), default_timeout=60).run()


def test_opens_on_the_question_with_a_computed_answer():
    at = _run()
    assert not at.exception
    assert at.title[0].value == content.QUESTION
    page = "\n".join(m.value for m in at.markdown)
    assert "Our answer" in "\n".join(s.value for s in at.subheader)
    assert "It depends on the scale" in page
    assert "tracked AI data centres" in page


def test_no_placeholder_is_left_on_the_page():
    at = _run()
    for element in at.markdown:
        assert "{" not in element.value and "}" not in element.value, element.value


def test_page_names_the_persona_and_limits():
    at = _run()
    page = "\n".join(m.value for m in at.markdown)
    assert "Priya" in page
    assert "Last data refresh" in page
    subheaders = [s.value for s in at.subheader]
    assert content.CANNOT_SHOW_TITLE in subheaders
    assert content.OTHER_SIDE_TITLE in subheaders
