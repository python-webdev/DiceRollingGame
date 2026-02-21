import random

# Step 1: Track how many completed rolls the player has made.
# Step 2: Keep the game running in a while loop until the player chooses to quit.
# Step 3: Ask if the player wants to roll or stop.
# Step 4: Ask how many dice to roll.
# Step 5: Validate that dice count is a valid number.
# Step 6: Enforce a minimum of 2 dice.
# Step 7: Roll each die, compute total, and format output text.
# Step 8: Check for doubles (all dice matching) for an extra turn.
# Step 9: Determine win/lose/draw from total score.
# Step 10: Show score, update completed roll count, and report progress.
# Step 11: Exit the game loop when player chooses to stop.
# Step 12: Handle invalid main-menu input.
# Step 13: Add Modes (Classic (normal dice), Lucky (win or doubles), Risk (if total < 7 lose points)))

roll_count = 0
modes = ["classic", "lucky", "risk"]

while True:
    user_input = input('Roll the dice? (y/n): ').lower()
    if user_input == 'y':
        dice_input = input('How many dice would you like to roll? ')
        try:
            if not dice_input.isdigit():
                raise ValueError(
                    'Invalid input. Dice count must be a number.')
            num_dice = int(dice_input)
            if num_dice < 2:
                raise ValueError('Dice count must be at least 2.')
        except ValueError as e:
            print(f'\n{e} Please try again.\n')
            continue

        mode_input = input('Choose a mode (Classic/Lucky/Risk): ').lower()

        try:
            if mode_input not in modes:
                raise ValueError("Invalid mode selected.")
        except ValueError as e:
            print(f'\n{e} Please choose from Classic, Lucky, or Risk.\n')
            continue

        dice_rolls = [random.randint(1, 6) for _ in range(num_dice)]
        total = sum(dice_rolls)
        rolled_numbers = ", ".join(map(str, dice_rolls))
        has_doubles = len(set(dice_rolls)) == 1

        if mode_input == "classic":
            if total > 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
            elif total == 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (It\'s a draw! Try again!)')
            else:
                print(
                    f'\nYou rolled: {rolled_numbers} (Sorry, you lose!)')

            print(f'Total score: {total}')
            roll_count += 1
            print(f'You have rolled the dice {roll_count} times. \n')

        if mode_input == "lucky":
            if has_doubles:
                print(
                    f'\nYou rolled: {rolled_numbers} (Doubles! You get an extra turn!)\n')
                continue  # Allow the player to roll again immediately
            if total > 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
            else:
                print(
                    f'\nYou rolled: {rolled_numbers} (Sorry, you lose!)')

            print(f'Total score: {total}')
            roll_count += 1
            print(f'You have rolled the dice {roll_count} times. \n')

        if mode_input == "risk":
            if total < 7:
                print(
                    f'\nYou rolled: {rolled_numbers} (Risky! You lose points!)')
            elif total > 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
            else:
                print(
                    f'\nYou rolled: {rolled_numbers} (It\'s a draw! Try again!)')

            print(f'Total score: {total}')
            roll_count += 1
            print(f'You have rolled the dice {roll_count} times. \n')

    elif user_input == 'n':
        print('\nThank you for playing! Goodbye!')
        break
    else:
        print("\nInvalid input. Please enter 'y' or 'n'.\n")
