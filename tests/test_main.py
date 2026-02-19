from dice_game.main import print_turn, main  # type: ignore


def test_print_turn_lucky_doubles(capsys):
    print_turn(
        mode="lucky",
        rolls=[3, 3],
        total=6,
        has_match=True,
        delta=5,
        points=10,
    )

    captured = capsys.readouterr()

    assert "Doubles! You get an extra turn!" in captured.out
    assert "Points +5" in captured.out
    assert "Total score: 6" in captured.out


def test_main_one_turn(monkeypatch, capsys):
    # simulate: y (play), then n (quit)
    inputs = iter(["y", "n"])
    monkeypatch.setattr("dice_game.main.ask_yes_no", lambda _: next(inputs))

    monkeypatch.setattr("dice_game.main.ask_int", lambda *args, **kwargs: 2)
    monkeypatch.setattr("dice_game.main.choose_mode", lambda: "normal")
    monkeypatch.setattr("dice_game.main.choose_dice_sides", lambda: 6)

    monkeypatch.setattr("dice_game.main.roll_dice", lambda n, s: [3, 4])
    monkeypatch.setattr("dice_game.main.all_match", lambda rolls: False)
    monkeypatch.setattr("dice_game.main.apply_points", lambda m, t, h: 2)

    main()

    captured = capsys.readouterr()

    assert "You rolled:" in captured.out
    assert "Current points: 2" in captured.out
