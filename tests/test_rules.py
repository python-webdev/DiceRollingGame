from src.dice_game.rules import outcome_from_total, apply_points


def test_outcome_from_total_win():
    assert outcome_from_total(11) == "win"
    assert outcome_from_total(30) == "win"


def test_outcome_from_total_draw():
    assert outcome_from_total(10) == "draw"


def test_outcome_from_total_lose():
    assert outcome_from_total(9) == "lose"
    assert outcome_from_total(0) == "lose"


def test_points_delta_classic_win_lose_draw():
    assert apply_points("classic", 11, has_match=False) == 5
    assert apply_points("classic", 10, has_match=False) == 0
    assert apply_points("classic", 9, has_match=False) == -3


def test_points_delta_lucky_match_bonus():
    # Lucky + match => +10 regardless of total
    assert apply_points("lucky", 2, has_match=True) == 10
    assert apply_points("lucky", 12, has_match=True) == 10


def test_points_delta_lucky_normal_when_no_match():
    assert apply_points("lucky", 11, has_match=False) == 5
    assert apply_points("lucky", 10, has_match=False) == 0
    assert apply_points("lucky", 9, has_match=False) == -3


def test_points_delta_risk_penalty_when_total_below_7():
    assert apply_points("risk", 6, has_match=False) == -3
    assert apply_points("risk", 1, has_match=True) == - \
        3  # penalty still applies


def test_points_delta_risk_normal_when_total_7_or_more():
    assert apply_points("risk", 11, has_match=False) == 5
    assert apply_points("risk", 10, has_match=False) == 0
    assert apply_points("risk", 9, has_match=False) == -3
