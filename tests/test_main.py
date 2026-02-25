# tests/test_main.py

from __future__ import annotations

from typing import ClassVar

import pytest

import dice_game.main as main_mod
from dice_game.main import (
    DiceGame,
    TurnDisplay,
    main,
    print_turn_outcome,
    print_turn_points,
)
from dice_game.stats import Stats


def make_ui(
    *,
    yes_no: list[str] | None = None,
    num_dice: int = 2,
    mode: str = "classic",
    sides: int = 6,
    rolls_text: str = "3, 4",
):
    """
    Returns a UI *class* (not instance) that satisfies UIProtocol.

    NOTE: This version expects UIProtocol methods to be @classmethod in src/dice_game/main.py.
    """
    answers = iter(yes_no or [])

    class FakeUI:
        _mode: ClassVar[str] = mode
        _sides: ClassVar[int] = sides
        _num_dice: ClassVar[int] = num_dice
        _rolls_text: ClassVar[str] = rolls_text

        @classmethod
        def ask_yes_no(cls, prompt: str) -> str:  # pylint: disable=unused-argument
            return next(answers, "n")

        @classmethod
        def ask_int(cls, prompt: str, *, min_value: int | None = None) -> int:  # pylint: disable=unused-argument
            if min_value is not None:
                assert cls._num_dice >= min_value
            return cls._num_dice

        @classmethod
        def choose_mode(cls) -> str:
            return cls._mode

        @classmethod
        def choose_dice_sides(cls) -> int:
            return cls._sides

        @classmethod
        def format_rolls(cls, rolls: list[int]) -> str:  # pylint: disable=unused-argument
            return cls._rolls_text

    return FakeUI


class DummyStats(Stats):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple[int, bool]] = []

    def update(self, total, has_match):
        super().update(total, has_match)
        self.calls.append((total, has_match))

    def summary_lines(self):
        return ["Turns: 1"]


def test_print_turn_outcome_lucky_match(monkeypatch, capsys):
    monkeypatch.setattr(
        main_mod.GameUI, "format_rolls", staticmethod(lambda _r: "3, 3")
    )

    turn = TurnDisplay(
        mode="lucky",
        rolls=[3, 3],
        total=6,
        has_match=True,
        delta=0,
        points=0,
    )

    repeat = print_turn_outcome(turn)
    out = capsys.readouterr().out

    assert "Doubles! You get an extra turn!" in out
    assert repeat is True


@pytest.mark.parametrize(
    "mode,total,outcome,expected",
    [
        ("risk", 6, "lose", "Risky! You lose points!"),
        ("classic", 12, "win", "Congratulations! You win!"),
        ("classic", 10, "draw", "It's a draw! Try again!"),
        ("classic", 2, "lose", "Sorry, you lose!"),
    ],
)
def test_print_turn_outcome_other_branches(
    monkeypatch, capsys, mode, total, outcome, expected
):
    monkeypatch.setattr(
        main_mod.GameUI, "format_rolls", staticmethod(lambda _r: "3, 4")
    )
    monkeypatch.setattr(
        main_mod.DiceGameRules, "outcome_from_total", lambda _self, _t: outcome
    )

    turn = TurnDisplay(
        mode=mode,
        rolls=[3, 4],
        total=total,
        has_match=False,
        delta=0,
        points=0,
    )

    repeat = print_turn_outcome(turn)
    out = capsys.readouterr().out

    assert expected in out
    assert repeat is False


@pytest.mark.parametrize(
    "delta,points,total,expected_line",
    [
        (5, 15, 10, "Points +5. Your current points: 15"),
        (-3, 7, 9, "Points -3. Your current points: 7"),
        (0, 10, 8, "Your current points: 10"),
    ],
)
def test_print_turn_points(delta, points, total, expected_line, capsys):
    print_turn_points(delta, points, total)
    out = capsys.readouterr().out

    assert expected_line in out
    assert f"Total score: {total}" in out


def test_play_turn_creates_dice_with_expected_type_and_updates_state(monkeypatch, capsys):
    ui = make_ui(num_dice=2, mode="classic", sides=6, rolls_text="3, 4")

    created = {"type": None}

    class FakeDice:
        def __init__(self, type):  # pylint: disable=redefined-builtin
            created["type"] = type

        def roll_dice(self, n):
            assert n == 2
            return [3, 4]

        def all_match(self, _rolls):
            return False

    monkeypatch.setattr(main_mod, "Dice", FakeDice)
    monkeypatch.setattr(
        main_mod.DiceGameRules, "apply_points", lambda _self, _mode, _total, _has_match: 2
    )
    monkeypatch.setattr(
        main_mod.DiceGameRules, "outcome_from_total", lambda _self, _total: "lose"
    )
    monkeypatch.setattr(
        main_mod.GameUI, "format_rolls", staticmethod(lambda _r: "3, 4")
    )
    monkeypatch.setattr(DiceGame, "print_progress", lambda _self: None)

    stats = DummyStats()
    game = DiceGame(ui=ui, stats=stats, min_dice=2)

    repeat = game.play_turn()
    out = capsys.readouterr().out

    assert created["type"] == "D6"
    assert stats.calls == [(7, False)]
    assert game.player_points == 2
    assert repeat is False
    assert "You rolled:" in out


def test_play_turn_returns_true_only_for_lucky_and_match(monkeypatch):
    ui = make_ui(num_dice=2, mode="lucky", sides=6, rolls_text="5, 5")

    class FakeDice:
        def __init__(self, **kwargs):
            self.type = kwargs.get("type")

        def roll_dice(self, _n):
            return [5, 5]

        def all_match(self, _rolls):
            return True

    monkeypatch.setattr(main_mod, "Dice", FakeDice)
    monkeypatch.setattr(
        main_mod.DiceGameRules, "apply_points", lambda _self, _mode, _total, _has_match: 10
    )
    monkeypatch.setattr(
        main_mod.GameUI, "format_rolls", staticmethod(lambda _r: "5, 5")
    )
    monkeypatch.setattr(DiceGame, "print_progress", lambda _self: None)

    game = DiceGame(ui=ui, stats=DummyStats())
    assert game.play_turn() is True


def test_run_quits_immediately(capsys):
    ui = make_ui(yes_no=["n"])

    game = DiceGame(ui=ui, stats=DummyStats())
    game.run()
    out = capsys.readouterr().out

    assert "Thank you for playing! Goodbye!" in out
    assert "Final points:" in out


def test_run_one_turn_then_quit(monkeypatch, capsys):
    ui = make_ui(yes_no=["y", "n"])

    game = DiceGame(ui=ui, stats=DummyStats())

    calls = {"n": 0}

    def fake_play_turn():
        calls["n"] += 1
        return False

    monkeypatch.setattr(game, "play_turn", fake_play_turn)

    game.run()
    out = capsys.readouterr().out

    assert calls["n"] == 1
    assert "Thank you for playing! Goodbye!" in out


def test_run_repeats_turn_on_extra_turn(monkeypatch):
    ui = make_ui(yes_no=["y", "y", "n"])

    game = DiceGame(ui=ui, stats=DummyStats())

    calls = {"n": 0}
    results = iter([True, False])

    def fake_play_turn():
        calls["n"] += 1
        return next(results)

    monkeypatch.setattr(game, "play_turn", fake_play_turn)

    game.run()
    assert calls["n"] == 2


def test_main_calls_run(monkeypatch):
    called = {"n": 0}

    def fake_run(_self):
        called["n"] += 1

    monkeypatch.setattr(main_mod.DiceGame, "run", fake_run)
    main()
    assert called["n"] == 1
