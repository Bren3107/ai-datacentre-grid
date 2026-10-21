"""Role C: README requirements; meaningful checks for the assessed content."""
from pathlib import Path
import re
from content import QUESTION

TEXT = (Path(__file__).resolve().parents[1] / 'README.md').read_text(encoding='utf-8-sig')

def test_question_persona_and_decision():
    assert QUESTION in TEXT
    assert 'Priya' in TEXT and 'regional energy planner' in TEXT
    assert 'priority in grid planning' in TEXT and 'another planning cycle' in TEXT

def test_three_stories_have_walkthroughs():
    stories = re.findall(r'^\d\. As a .+, I want .+, so that .+$', TEXT, re.M)
    assert len(stories) == 3
    assert TEXT.count('Walk-through:') == 3
    for control in ['Regions', 'Countries', 'Owners', 'Minimum IT power (MW)', 'Show the numbers']:
        assert control in TEXT

def test_four_chart_families_and_units():
    for family in ['Change over time', 'Ranking', 'Part-to-whole', 'Distribution']:
        assert family in TEXT
    for chart in ['C1:', 'C2:', 'C3:', 'C4:']:
        assert chart in TEXT
    assert 'estimated IT power' in TEXT
    assert 'TODO' not in TEXT and 'DRAFT' not in TEXT
