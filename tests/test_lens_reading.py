"""Role D: one test per ratio branch of the Scale lens, plus the 'up from / down from' word."""
import content


def test_two_or_more_matters_for_planning():
    for ratio in (2.0, 2.7, 3.2):
        assert content.reading_key(ratio) == "matter"
    assert "large enough to matter for planning" in content.LENS_ENTITY_READING["matter"]


def test_one_to_under_two_is_above_the_world_average():
    for ratio in (1.0, 1.2, 1.9999):
        assert content.reading_key(ratio) == "above"
    assert "above the world average" in content.LENS_ENTITY_READING["above"]


def test_under_one_is_below_the_world_average():
    for ratio in (0.0, 0.08, 0.73, 0.9999):
        assert content.reading_key(ratio) == "below"
    assert "below the world average" in content.LENS_ENTITY_READING["below"]


def test_every_reading_is_labelled_as_ours():
    for sentence in content.LENS_ENTITY_READING.values():
        assert sentence.startswith("Our reading:")
    assert content.LENS_WORLD["reading"].startswith("Our reading:")
    assert content.LENS_SITE["reading"].startswith("Our reading:")


def test_change_word_follows_the_values_shown():
    assert content.change_word(2.64, 4.94) == "up from"
    assert content.change_word(0.50, 0.30) == "down from"
    assert content.change_word(0.12, 0.12) == "level with"
    assert content.change_word(0.121, 0.124) == "level with"  # both show as 0.1
