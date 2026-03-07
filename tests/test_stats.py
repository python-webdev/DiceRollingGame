from dice_game.domain.stats import Stats


def test_initial_state():
    stats = Stats()
    assert stats.roll_count == 0
    assert stats.total_doubles == 0
    assert stats.total_roll_value == 0
    assert stats.highest_roll == 0
    assert stats.lowest_roll is None


def test_update_increments_roll_count_and_total():
    stats = Stats()
    stats.update(total=7, has_match=False)

    assert stats.roll_count == 1
    assert stats.total_roll_value == 7


def test_update_tracks_highest_and_lowest():
    stats = Stats()

    stats.update(total=7, has_match=False)
    stats.update(total=12, has_match=False)
    stats.update(total=5, has_match=False)

    assert stats.highest_roll == 12
    assert stats.lowest_roll == 5


def test_update_tracks_doubles():
    stats = Stats()

    stats.update(total=8, has_match=False)
    stats.update(total=6, has_match=True)
    stats.update(total=10, has_match=True)

    assert stats.total_doubles == 2


def test_average_no_rolls():
    stats = Stats()
    assert stats.average == 0.0


def test_average_correct_value():
    stats = Stats()
    stats.update(total=10, has_match=False)
    stats.update(total=20, has_match=False)

    assert stats.average == 15.0


def test_summary_no_rolls():
    stats = Stats()
    stats.print_stats(points_total=0)  # Should print "No rolls yet."
