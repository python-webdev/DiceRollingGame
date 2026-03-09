from dice_game.storage.sqlite_storage import export_rolls_to_csv


def test_csv_export_creates_file(tmp_path):
    filepath = tmp_path / "rolls_export.csv"

    export_rolls_to_csv(filepath)

    assert filepath.exists()


def test_csv_contains_headers(tmp_path):
    filepath = tmp_path / "rolls_export.csv"

    export_rolls_to_csv(filepath)

    test = filepath.read_text()

    assert "id,time,mode" in test
