from src.dice_game.dice import all_match


def test_all_match_true_for_same_values():
    assert all_match([3, 3]) is True
    assert all_match([6, 6, 6]) is True


def test_all_match_false_for_mixed_values():
    assert all_match([3, 4]) is False
    assert all_match([1, 2, 1]) is False


def test_all_match_single_value_is_true():
    # Not used in game (you require 2+ dice), but function should behave sensibly.
    assert all_match([5]) is True
