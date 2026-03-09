from dice_game.storage.sqlite_storage import paginated_rolls


def test_first_page_returns_rows():
    rows = paginated_rolls(offset=0, limit=10)

    assert isinstance(rows, list)


def test_offset_beyond_rows_returns_empty():
    rows = paginated_rolls(offset=1000, limit=10)

    assert rows == []
