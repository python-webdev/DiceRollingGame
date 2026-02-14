import random
# Add total score.
roll_count = 0
while True:
    user_input = input('Roll the dice? (y/n): ').lower()
    if user_input == 'y':
        dice_input = input('How many dice would you like to roll? ')
        # Validate num_dice input to ensure it's number and at least 2 dice
        try:
            num_dice = int(dice_input)
        except (TypeError, ValueError):
            print('Invalid input. Please enter a number for the dice count.')
            continue
        if num_dice < 2:
            print('Dice count must be at least 2. Please try again.')
            continue
        dice_rolls = [random.randint(1, 6) for _ in range(num_dice)]
        total = sum(dice_rolls)
        rolled_numbers = ", ".join(map(str, dice_rolls))
        # Check if all dice show the same number (doubles)
        has_doubles = len(set(dice_rolls)) == 1
        if has_doubles:  # All dice show the same number
            print(
                f'\nYou rolled: {rolled_numbers} (Doubles! You get an extra turn!)')
            continue  # Allow the player to roll again immediately
        if total > 10:
            print(
                f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
        elif total < 5:
            print(
                f'\nYou rolled: {rolled_numbers} (Sorry, you lose!)')
        else:
            print(
                f'\nYou rolled: {rolled_numbers} (It\'s a draw!)')
        print(f'Total score: {total}')
        roll_count += 1
        print(f'You have rolled the dice {roll_count} times. \n')
    elif user_input == 'n':
        print('Thank you for playing! Goodbye!')
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
