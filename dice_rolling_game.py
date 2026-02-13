import random

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
        dice1, dice2 = dice_rolls[:2]  # Get the first two dice rolls
        print(f'You rolled: {dice1} and {dice2}')
        roll_count += 1
        if dice1 == dice2:
            print('Congratulations! You rolled doubles!')
        print(f'You have rolled the dice {roll_count} times.')
    elif user_input == 'n':
        print('Thank you for playing! Goodbye!')
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
