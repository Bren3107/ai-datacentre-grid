"""Role A: processed files regenerate byte for byte from the raw files (marking check 5.6).

The script writes into a temporary folder here, so the test never touches data/processed/.
CI also reruns the script in place and fails if `git status --porcelain data/processed` shows anything.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_processed.py"
PROCESSED = ROOT / "data" / "processed"
GENERATED = ["dc_share.csv", "sites.csv", "capacity_timeline.csv", "meta.json"]


def run_script(out_dir):
    subprocess.run([sys.executable, str(SCRIPT), "--out", str(out_dir)], check=True, cwd=ROOT)


def test_script_reproduces_the_committed_files(tmp_path):
    run_script(tmp_path)
    for name in GENERATED:
        assert (tmp_path / name).read_bytes() == (PROCESSED / name).read_bytes(), f"{name} differs"


def test_second_run_changes_nothing(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    run_script(first)
    run_script(second)
    for name in GENERATED:
        assert (first / name).read_bytes() == (second / name).read_bytes(), f"{name} differs between runs"


def test_files_use_unix_newlines_only():
    for name in GENERATED:
        assert b"\r\n" not in (PROCESSED / name).read_bytes(), f"{name} has CRLF line endings"
