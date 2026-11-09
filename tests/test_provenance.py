"""Role D: the provenance matrix has a complete row for every member (checks 5.4)."""
from pathlib import Path

PROVENANCE = Path(__file__).resolve().parents[1] / "docs" / "PROVENANCE.md"
MEMBERS = ("Brendan", "Daniel", "yux7540-design", "Avishek")
COLUMNS = ["Artefact", "Who", "Tool", "What was asked", "What came back",
           "How it was verified", "Outcome"]
# A verification must name something that could have failed.
CHECK_WORDS = ("fail", "test", "recomput", "compar", "break", "check", "exit", "measur")


def rows():
    out = []
    for line in PROVENANCE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith("|---"):
            out.append([c.strip() for c in line.strip().strip("|").split(" | ")])
    header, body = out[0], out[1:]
    return header, body


def test_header_has_the_seven_columns():
    header, _ = rows()
    assert header == COLUMNS


def test_every_row_is_complete():
    _, body = rows()
    assert body, "no rows"
    for row in body:
        assert len(row) == len(COLUMNS), f"row has {len(row)} cells: {row[0][:50]}"
        assert all(row), f"empty cell in row: {row[0][:50]}"


def test_every_member_has_at_least_one_row():
    _, body = rows()
    for member in MEMBERS:
        assert any(row[1].startswith(member) for row in body), f"no row for {member}"


def test_every_verification_names_a_check():
    _, body = rows()
    for row in body:
        verification = row[5].lower()
        assert len(verification) > 60, f"verification too short: {row[0][:50]}"
        assert any(word in verification for word in CHECK_WORDS), row[0][:50]


def test_no_placeholder_cells():
    _, body = rows()
    for row in body:
        for cell in row:
            assert cell.upper() not in ("TODO", "TBD", "..."), row[0][:50]
