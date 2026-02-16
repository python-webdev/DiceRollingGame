# DiceRollingGame

A lightweight Dice Rolling application exploring RNG (Random Number Generation) and event-driven logic with multiple game modes for varied gameplay experiences. Features comprehensive statistics tracking and a dynamic point system.

## Features

- **Three Game Modes**: Classic, Lucky, and Risk modes with unique rules
- **Point System**: Earn and lose points based on performance
- **Comprehensive Statistics**: Track rolls, averages, doubles, and extremes
- **Input Validation**: Robust error handling for user inputs
- **Continuous Play**: Roll until you choose to quit

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
- Main menu accepts only 'y' or 'n'
- Invalid inputs prompt retry with helpful messages
