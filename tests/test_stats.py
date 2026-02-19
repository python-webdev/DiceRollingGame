from dice_game.stats import Stats


def test_stats_update_increments_roll_count():
    s = Stats()
    s.update(total=9, has_match=False)
    assert s.roll_count == 1


def test_stats_update_tracks_total_roll_value_and_average():
    s = Stats()
    s.update(total=10, has_match=False)
    s.update(total=6, has_match=False)
    assert s.total_roll_value == 16
    assert s.average() == 8.0


def test_stats_update_tracks_highest_and_lowest():
    s = Stats()
    s.update(total=12, has_match=False)
    s.update(total=7, has_match=False)
    s.update(total=20, has_match=False)
    assert s.highest_roll == 20
    assert s.lowest_roll == 7


def test_stats_update_tracks_doubles():
    s = Stats()
    s.update(total=8, has_match=True)
    s.update(total=9, has_match=False)
    assert s.total_doubles == 1


def test_stats_summary_lines_no_rolls():
    s = Stats()
    lines = s.summary_lines()
    assert lines == ["No rolls yet."]


def test_stats_summary_lines_with_rolls_contains_expected_fields():
    s = Stats()
    s.update(total=10, has_match=True)
    lines = s.summary_lines()
    joined = "\n".join(lines)

    assert "rolled the dice 1 times" in joined
    assert "Average roll value" in joined
    assert "Total doubles rolled" in joined
    assert "Highest roll" in joined
    assert "Lowest roll" in joined
