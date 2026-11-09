"""Role D: the disclosure statement is present, finished and does not overclaim (check 5.5)."""
from pathlib import Path

DISCLOSURE = Path(__file__).resolve().parents[1] / "docs" / "DISCLOSURE.md"
TEXT = DISCLOSURE.read_text(encoding="utf-8")
MEMBERS = {
    "Brendan": ("Brendan",),
    "Daniel": ("Daniel", "Dan "),
    "Ming": ("yux7540-design", "Xiangqiang", "Ming"),
    "Avishek": ("Avishek",),
}


def test_no_todo_or_placeholder_left():
    assert "TODO" not in TEXT
    assert "{" not in TEXT and "<<" not in TEXT


def test_has_the_three_sections():
    for heading in ("## Data", "## AI use", "## Declaration"):
        assert heading in TEXT, heading


def test_every_member_is_named_in_the_tools_and_in_a_confirmation_line():
    lines = TEXT.splitlines()
    for member, aliases in MEMBERS.items():
        tools = [l for l in lines if l.startswith("  - ") and any(a in l.split(":")[0] for a in aliases)]
        assert tools, f"{member} missing from tools used"
        confirms = [l for l in lines if l.startswith("- ") and "confirmed" in l and any(a in l.split(":")[0] for a in aliases)]
        assert confirms, f"{member} missing from confirmations"


def test_processing_bullet_does_not_overclaim():
    # Reviewer point on PR #8: chart values are computed in charts/, not in facts.py.
    assert "Every number on the page is computed in" not in TEXT
    assert "charts/*.py" in TEXT and "Show the numbers" in TEXT


def test_not_delegated_bullet_mentions_the_build_plan():
    assert "BUILD_PLAN.md" in TEXT and "Claude Code" in TEXT


def test_points_to_the_other_documents():
    for name in ("DATA_DICTIONARY.md", "PROVENANCE.md"):
        assert name in TEXT
