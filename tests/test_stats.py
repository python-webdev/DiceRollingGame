from dice_game.stats import Stats


def test_initial_state():
    stats = Stats()
    assert stats.roll_count == 0
    assert stats.total_doubles == 0
    assert stats.total_roll_value == 0
    assert stats.highest_roll == 0
    assert stats.lowest_roll is None


def test_update_increments_roll_count_and_total():
    stats = Stats()
    stats.update(total=7, has_match=False, count_roll=True)

    assert stats.roll_count == 1
    assert stats.total_roll_value == 7


def test_update_tracks_highest_and_lowest():
    stats = Stats()

    stats.update(total=7, has_match=False, count_roll=True)
    stats.update(total=12, has_match=False, count_roll=True)
    stats.update(total=5, has_match=False, count_roll=True)

    assert stats.highest_roll == 12
    assert stats.lowest_roll == 5


def test_update_tracks_doubles():
    stats = Stats()

    stats.update(total=8, has_match=False, count_roll=True)
    stats.update(total=6, has_match=True, count_roll=True)
    stats.update(total=10, has_match=True, count_roll=True)

    assert stats.total_doubles == 2


def test_average_no_rolls():
    stats = Stats()
    assert stats.average() == 0.0


def test_average_correct_value():
    stats = Stats()
    stats.update(total=10, has_match=False, count_roll=True)
    stats.update(total=20, has_match=False, count_roll=True)

    assert stats.average() == 15.0


def test_summary_no_rolls():
    stats = Stats()
    lines = stats.summary_lines()

    assert lines == ["No rolls yet."]


def test_summary_after_updates():
    stats = Stats()
    stats.update(total=10, has_match=False, count_roll=True)
    stats.update(total=20, has_match=True, count_roll=True)

    lines = stats.summary_lines()

    assert len(lines) == 5
    assert "You have rolled the dice 2 times." in lines[0]
    assert "Average roll value: 15.00" in lines[1]
    assert "Total doubles rolled: 1" in lines[2]
    assert "Highest roll: 20" in lines[3]
    assert "Lowest roll: 10" in lines[4]
