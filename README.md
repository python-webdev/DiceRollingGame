# DiceRollingGame

A lightweight Dice Rolling application exploring RNG (Random Number Generation) and event-driven logic.

## How it works

1. The game starts by setting a counter for completed rolls.
2. It repeatedly asks: `Roll the dice? (y/n)`.
3. If you enter `y`, it asks how many dice to roll.
4. The dice count is validated:
    - Must be a number
    - Must be at least 2
5. The game rolls the selected number of dice (`1` to `6`) and sums the total.
6. If all dice match (doubles), you get an extra turn immediately.
7. If not doubles, outcome is decided by total:
    - `> 10`: Win
    - `< 5`: Lose
    - Otherwise: Draw
8. It prints your total score and increments the completed-roll counter.
9. If you enter `n` at the main prompt, the game exits with a goodbye message.
10. Any invalid menu input prompts you to enter `y` or `n`.
