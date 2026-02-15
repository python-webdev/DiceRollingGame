# DiceRollingGame

A lightweight Dice Rolling application exploring RNG (Random Number Generation) and event-driven logic with multiple game modes for varied gameplay experiences.

## Game Modes

The game features three distinct modes, each with unique rules and outcomes:

### Classic Mode
- Traditional dice rolling experience
- **Win**: Total > 10
- **Draw**: Total = 10  
- **Lose**: Total < 10

### Lucky Mode
- Features special doubles mechanic
- **Doubles**: If all dice match, get an extra turn immediately!
- **Win**: Total > 10 (if no doubles)
- **Lose**: Total ≤ 10 (if no doubles)

### Risk Mode
- High-stakes gameplay with penalty for low rolls
- **Risky Loss**: Total < 7 (lose points!)
- **Win**: Total > 10
- **Draw**: Total 7-10

## How it works

1. The game starts by setting a counter for completed rolls.
2. It repeatedly asks: `Roll the dice? (y/n)`.
3. If you enter `y`, it asks how many dice to roll.
4. The dice count is validated:
    - Must be a number
    - Must be at least 2
5. You choose a game mode: Classic, Lucky, or Risk.
6. The game rolls the selected number of dice (`1` to `6`) and sums the total.
7. The outcome is determined based on your selected mode's rules (see above).
8. It prints your total score and increments the completed-roll counter.
9. If you enter `n` at the main prompt, the game exits with a goodbye message.
10. Any invalid input (menu choice or mode selection) prompts you to try again.
