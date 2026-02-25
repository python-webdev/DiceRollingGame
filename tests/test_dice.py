import pytest
from dice_game.dice import Dice, DICE_TYPES


# ---------- DICE_TYPES ----------


def test_dice_types_contains_expected_values():
    assert DICE_TYPES["D4"] == 4
    assert DICE_TYPES["D6"] == 6
    assert DICE_TYPES["D20"] == 20


def test_dice_types_keys_are_uppercase():
    for key in DICE_TYPES:
        assert key.isupper()


def test_dice_sets_sides_from_type():
    d = Dice(type="D20")
    assert d.sides == 20


def test_invalid_dice_type_raises():
    with pytest.raises(ValueError):
        Dice(type="D100")


# ---------- roll_dice ----------

def test_roll_dice_returns_correct_length(monkeypatch):
    # Force deterministic value
    monkeypatch.setattr("dice_game.dice.random.randint", lambda a, b: 3)

    dice = Dice()
    rolls = dice.roll_dice(5)

    assert len(rolls) == 5
    assert rolls == [3, 3, 3, 3, 3]


def test_roll_dice_calls_randint_with_correct_bounds(monkeypatch):
    calls = []

    def fake_randint(a, b):
        calls.append((a, b))
        return 1

    monkeypatch.setattr("dice_game.dice.random.randint", fake_randint)

    dice = Dice()
    dice.roll_dice(3)

    assert calls == [(1, 6), (1, 6), (1, 6)]


# ---------- all_match ----------

def test_all_match_true():
    dice = Dice()
    assert dice.all_match([5, 5, 5]) is True


def test_all_match_false():
    dice = Dice()
    assert dice.all_match([5, 4, 5]) is False


def test_all_match_single_value():
    dice = Dice()
    assert dice.all_match([3]) is True


def test_all_match_empty_list():
    dice = Dice()
    assert dice.all_match([]) is False
