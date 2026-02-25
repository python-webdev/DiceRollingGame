import pytest

from dice_game.rules import DiceGameRules, rules, modes


@pytest.mark.parametrize(
    "total, expected",
    [
        (0, "lose"),
        (9, "lose"),
        (10, "draw"),
        (11, "win"),
        (999, "win"),
    ],
)
def test_outcome_from_total(total, expected):
    r = DiceGameRules()
    assert r.outcome_from_total(total) == expected


def test_modes_constant():
    assert DiceGameRules.MODES == {"classic", "lucky", "risk"}
    assert modes == {"classic", "lucky", "risk"}


def test_rules_instance():
    assert isinstance(rules, DiceGameRules)


def test_apply_points_lucky_match_overrides_everything():
    r = DiceGameRules()
    # even if total would be lose or risk, lucky+match must return 10
    assert r.apply_points("lucky", total=2, has_match=True) == 10
    assert r.apply_points("lucky", total=100, has_match=True) == 10


@pytest.mark.parametrize(
    "total",
    [0, 1, 2, 3, 4, 5, 6],
)
def test_apply_points_risk_total_below_7_is_minus_3(total):
    r = DiceGameRules()
    assert r.apply_points("risk", total=total, has_match=False) == -3


def test_apply_points_risk_total_7_or_more_falls_back_to_outcome():
    r = DiceGameRules()
    # total 7 -> outcome is lose (<10) -> -3
    assert r.apply_points("risk", total=7, has_match=False) == -3
    # total 10 -> draw -> 0
    assert r.apply_points("risk", total=10, has_match=False) == 0
    # total 11 -> win -> +5
    assert r.apply_points("risk", total=11, has_match=False) == 5


@pytest.mark.parametrize(
    "mode,total,expected",
    [
        ("classic", 9, -3),   # lose
        ("classic", 10, 0),   # draw
        ("classic", 11, 5),   # win
        ("lucky", 9, -3),     # lucky without match falls back to outcome
        ("lucky", 10, 0),
        ("lucky", 11, 5),
    ],
)
def test_apply_points_non_special_cases(mode, total, expected):
    r = DiceGameRules()
    assert r.apply_points(mode, total=total, has_match=False) == expected
