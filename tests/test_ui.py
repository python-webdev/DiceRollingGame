import builtins

from dice_game.ui import GameUI


def _patch_inputs(monkeypatch, values):
    it = iter(values)
    monkeypatch.setattr(builtins, "input", lambda _: next(it))


# ---------------- ask_yes_no ----------------

def test_ask_yes_no_accepts_y(monkeypatch):
    _patch_inputs(monkeypatch, ["y"])
    assert GameUI.ask_yes_no("Roll? ") == "y"


def test_ask_yes_no_accepts_n(monkeypatch):
    _patch_inputs(monkeypatch, ["n"])
    assert GameUI.ask_yes_no("Roll? ") == "n"


def test_ask_yes_no_reprompts_on_invalid_then_accepts(monkeypatch, capsys):
    _patch_inputs(monkeypatch, ["maybe", "Y"])  # should lower() to "y"
    assert GameUI.ask_yes_no("Roll? ") == "y"

    out = capsys.readouterr().out
    assert "Invalid input" in out


# ---------------- ask_int ----------------

def test_ask_int_parses_int(monkeypatch):
    _patch_inputs(monkeypatch, ["42"])
    assert GameUI.ask_int("How many? ") == 42


def test_ask_int_reprompts_on_non_number(monkeypatch, capsys):
    _patch_inputs(monkeypatch, ["abc", "5"])
    assert GameUI.ask_int("How many? ") == 5

    out = capsys.readouterr().out
    assert "Invalid input. Please enter a valid number." in out


def test_ask_int_enforces_min_value(monkeypatch, capsys):
    _patch_inputs(monkeypatch, ["1", "2"])
    assert GameUI.ask_int("How many? ", min_value=2) == 2

    out = capsys.readouterr().out
    assert "Dice count must be at least 2" in out


# ---------------- choose_mode ----------------

def test_choose_mode_accepts_valid(monkeypatch):
    _patch_inputs(monkeypatch, ["classic"])
    assert GameUI.choose_mode() == "classic"


def test_choose_mode_reprompts_on_invalid(monkeypatch, capsys):
    _patch_inputs(monkeypatch, ["wrong", "Lucky"])  # Lucky -> "lucky"
    assert GameUI.choose_mode() == "lucky"

    out = capsys.readouterr().out
    assert "Invalid mode" in out


# ---------------- choose_dice_sides ----------------

def test_choose_dice_sides_accepts_valid(monkeypatch):
    _patch_inputs(monkeypatch, ["D6"])
    assert GameUI.choose_dice_sides() == 6


def test_choose_dice_sides_accepts_lowercase(monkeypatch):
    _patch_inputs(monkeypatch, ["d20"])
    assert GameUI.choose_dice_sides() == 20


def test_choose_dice_sides_reprompts_on_invalid(monkeypatch, capsys):
    _patch_inputs(monkeypatch, ["D100", "D4"])
    assert GameUI.choose_dice_sides() == 4

    out = capsys.readouterr().out
    assert "Invalid dice type" in out


# ---------------- format_rolls ----------------

def test_format_rolls():
    assert GameUI.format_rolls([1, 2, 10]) == "1, 2, 10"


# ---------------- wrapper functions forward correctly ----------------

def test_wrapper_ask_yes_no_calls_class(monkeypatch):
    monkeypatch.setattr(GameUI, "ask_yes_no",
                        staticmethod(lambda prompt: "y"))
    assert GameUI.ask_yes_no("x") == "y"


def test_wrapper_ask_int_calls_class(monkeypatch):
    monkeypatch.setattr(GameUI, "ask_int", staticmethod(
        lambda prompt, min_value=None: 3))
    assert GameUI.ask_int("x", min_value=2) == 3


def test_wrapper_choose_mode_calls_class(monkeypatch):
    monkeypatch.setattr(GameUI, "choose_mode", staticmethod(lambda: "risk"))
    assert GameUI.choose_mode() == "risk"


def test_wrapper_choose_dice_sides_calls_class(monkeypatch):
    monkeypatch.setattr(GameUI, "choose_dice_sides", staticmethod(lambda: 8))
    assert GameUI.choose_dice_sides() == 8


def test_wrapper_format_rolls_calls_class(monkeypatch):
    monkeypatch.setattr(GameUI, "format_rolls",
                        staticmethod(lambda rolls: "X"))
    assert GameUI.format_rolls([1, 2]) == "X"
