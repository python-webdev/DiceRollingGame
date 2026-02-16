# DiceRollingGame

A lightweight Dice Rolling application exploring RNG (Random Number Generation) and event-driven logic with multiple game modes for varied gameplay experiences. Features comprehensive statistics tracking and a dynamic point system.

## Features

- **Three Game Modes**: Classic, Lucky, and Risk with distinct scoring rules
- **Multiple Dice Types**: Choose from D4, D6, D8, D10, D12, or D20
- **Dynamic Round Setup**: Select how many dice to roll (minimum 2)
- **Point Tracking**: Gain/lose points across rounds based on outcomes
- **Live Statistics**: Shows roll count, doubles, average, highest, and lowest values
- **Input Validation**: Handles invalid yes/no, dice count, mode, and dice type entries

## Game Flow

This is the round flow in the order the script executes:

1. Game starts and initializes counters (rolls, points, doubles, roll stats).
2. Prompt appears: `Roll the dice? (y/n)`.
3. If `n`, game exits with a goodbye message.
4. If `y`, player enters number of dice.
5. Dice count is validated (must be numeric and at least 2).
6. Player chooses mode: `Classic`, `Lucky`, or `Risk`.
7. Mode is validated.
8. Player chooses dice type: `D4`, `D6`, `D8`, `D10`, `D12`, or `D20`.
9. Dice type is validated and mapped to number of sides.
10. Script rolls all selected dice and calculates total score.
11. Script checks for doubles (all dice values matching).
12. Mode-specific win/lose/draw rules are applied and points are updated.
13. In Lucky mode, doubles grant +10 points and an immediate extra turn.
14. Roll count and statistics are displayed after completed rounds.
15. Loop continues until player chooses `n` at the main prompt.

## Game Modes

The game features three distinct modes, each with unique rules and outcomes:

### Classic Mode

- Traditional dice rolling experience
- **Win**: Total > 10 (+5 points)
- **Draw**: Total = 10 (no points)
- **Lose**: Total < 10 (-3 points)

### Lucky Mode

- Features special doubles mechanic
- **Doubles**: If all dice match, get +10 points and an extra turn immediately!
- **Win**: Total > 10 (+5 points)
- **Draw**: Total = 10 (no points)
- **Lose**: Total < 10 (-3 points)

### Risk Mode

- High-stakes gameplay with penalty for low rolls
- **Risky Loss**: Total < 7 (-3 points)
- **Win**: Total > 10 (+5 points)
- **Draw**: Total 7-10 (no points)

## Point System

- **+10 points**: Rolling doubles (all dice same value) in Lucky mode
- **+5 points**: Winning a round (total > 10)
- **-3 points**: Losing a round or rolling risky (total < 7 in Risk mode)

## Statistics Tracked

The game automatically tracks and displays:

- **Roll Count**: Total number of completed rolls
- **Player Points**: Current point balance
- **Average Roll**: Mean value across all rolls
- **Total Doubles**: Number of times all dice matched
- **Highest Roll**: Maximum total achieved
- **Lowest Roll**: Minimum total achieved

## How to Play

1. Run the game: `python dice_rolling_game.py`
2. Choose to roll dice or quit: `Roll the dice? (y/n)`
3. If rolling, specify number of dice (minimum 2)
4. Select a game mode: Classic, Lucky, or Risk
5. View your results, points, and statistics
6. Continue playing or quit

## Requirements

- Python 3.x
- No external dependencies (uses built-in `random` module)

## Installation & Usage

```bash
# Clone or download the file
python dice_rolling_game.py
```

## Input Validation

The game includes robust input validation:

- Dice count must be a valid number ≥ 2
- Game mode must be one of: classic, lucky, risk
- Dice type must be one of: D4, D6, D8, D10, D12, D20
- Main menu accepts only 'y' or 'n'
- Invalid inputs prompt retry with helpful messages
