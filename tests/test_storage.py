from dice_game.storage.roll_repository import count_rolls


def test_empty_database_has_zero_rows():
    """Test that a fresh database has no rolls."""
    assert count_rolls() == 0
