from dice_game.ui import ask_yes_no, ask_int, choose_mode, choose_dice_sides, format_rolls


def test_ask_yes_no_valid_inputs(monkeypatch):
    inputs = iter(["y", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert ask_yes_no("Roll the dice? (y/n): ") == "y"
    assert ask_yes_no("Roll the dice? (y/n): ") == "n"


def test_ask_yes_no_invalid_then_valid(monkeypatch):
    inputs = iter(["maybe", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert ask_yes_no("Roll the dice? (y/n): ") == "y"


def test_ask_int_valid_inputs(monkeypatch):
    inputs = iter(["5", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert ask_int("Enter a number: ") == 5
    assert ask_int("Enter a number: ") == 10


def test_ask_int_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["abc", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = ask_int("Enter a number: ")
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out
    assert result == 5


def test_ask_int_below_min_then_valid(monkeypatch, capsys):
    inputs = iter(["1", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = ask_int("Enter a number: ", min_value=2)
    captured = capsys.readouterr()
    assert "Value must be at least 2" in captured.out
    assert result == 5


def test_choose_mode_valid_inputs(monkeypatch):
    inputs = iter(["Classic", "Lucky", "Risk"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert choose_mode() == "classic"
    assert choose_mode() == "lucky"
    assert choose_mode() == "risk"


def test_choose_mode_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["InvalidMode", "Classic"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = choose_mode()
    captured = capsys.readouterr()
    assert "Invalid mode" in captured.out
    assert result == "classic"


def test_choose_dice_sides_valid_inputs(monkeypatch):
    inputs = iter(["D4", "D6", "D8", "D10", "D12", "D20"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert choose_dice_sides() == 4
    assert choose_dice_sides() == 6
    assert choose_dice_sides() == 8
    assert choose_dice_sides() == 10
    assert choose_dice_sides() == 12
    assert choose_dice_sides() == 20


def test_choose_dice_sides_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["InvalidDice", "D6"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = choose_dice_sides()
    captured = capsys.readouterr()
    assert "Invalid dice type" in captured.out
    assert result == 6


def test_format_rolls():
    rolls = [3, 5, 2]
    formatted = format_rolls(rolls)
    assert formatted == "3, 5, 2"
