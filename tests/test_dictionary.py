"""Role A: docs/DATA_DICTIONARY.md covers every data file with the fields the brief lists (check 5.2)."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DICTIONARY = ROOT / "docs" / "DATA_DICTIONARY.md"
FIELDS = [
    "Source",
    "Licence",
    "Columns and units",
    "Primary key",
    "Time coverage",
    "Latest observation",
    "Retrieved on",
    "Transform",
]
DATA_FILES = sorted(
    p.relative_to(ROOT).as_posix()
    for folder in ("data/raw", "data/processed")
    for p in (ROOT / folder).iterdir()
    if p.suffix in (".csv", ".json")
)


def sections():
    """Map '## heading' -> body text."""
    parts = re.split(r"^## ", DICTIONARY.read_text(encoding="utf-8"), flags=re.M)[1:]
    return {p.splitlines()[0].strip(): p for p in parts}


def test_no_todo_left():
    assert "TODO" not in DICTIONARY.read_text(encoding="utf-8")


def test_every_data_file_has_a_section():
    headings = " ".join(sections())
    missing = [f for f in DATA_FILES if f not in headings]
    assert not missing, f"no dictionary section for {missing}"


@pytest.mark.parametrize("data_file", DATA_FILES)
def test_section_has_every_field_filled(data_file):
    body = next(text for heading, text in sections().items() if data_file in heading)
    for field in FIELDS:
        match = re.search(rf"^\| {re.escape(field)}[^|]* \| (.+) \|$", body, flags=re.M)
        assert match, f"{data_file}: field '{field}' missing"
        assert match.group(1).strip(), f"{data_file}: field '{field}' empty"


def test_the_four_open_questions_are_answered():
    text = DICTIONARY.read_text(encoding="utf-8")
    for n in range(1, 5):
        assert re.search(rf"^{n}\. \*\*", text, flags=re.M), f"question {n} not answered"
