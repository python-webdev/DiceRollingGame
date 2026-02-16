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
# Step 14: Add Player Points to track score across rounds (e.g +10 for points double, +5 if total > 8, -3 if total < 5)
# Step 15: Add Statistics (total rolls, total doubles, average roll value, highest roll, lowest roll)
# Step 16: Add dice types (e.g. D4, D6, D8, D10, D12, D20) and allow player to choose which type of dice to roll.

roll_count = 0
player_points = 0
total_doubles = 0
total_roll_value = 0
highest_roll = 0
lowest_roll = 0
modes = ["classic", "lucky", "risk"]

while True:
    user_input = input('Roll the dice? (y/n): ').lower()
    if user_input == 'y':
        dice_input = input('How many dice would you like to roll? ')
        if not dice_input.isdigit():
            print('\nInvalid input. Please enter a valid number for dice count.\n')
            continue
        num_dice = int(dice_input)
        if num_dice < 2:
            print('\nDice count must be at least 2. Please try again.\n')
            continue
        mode_input = input('Choose a mode (Classic/Lucky/Risk): ').lower()
        if mode_input not in modes:
            print('\nInvalid mode. Please select a valid mode.\n')
            continue

        dice_type_input = input(
            'Choose a dice type (D4, D6, D8, D10, D12, D20): ').upper()
        dice_types = {"D4": 4, "D6": 6, "D8": 8,
                      "D10": 10, "D12": 12, "D20": 20}
        if dice_type_input not in dice_types:
            print('\nInvalid dice type. Please select a valid dice type.\n')
            continue
        dice_sides = dice_types[dice_type_input]

        dice_rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
        total = sum(dice_rolls)
        total_roll_value += total
        highest_roll = max(highest_roll, total)
        lowest_roll = float('inf')
        lowest_roll = min(lowest_roll, total)
        if len(set(dice_rolls)) == 1:
            total_doubles += 1
        rolled_numbers = ", ".join(map(str, dice_rolls))

        has_doubles = len(set(dice_rolls)) == 1
        if mode_input == "classic":
            if total > 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
                player_points += 5  # Award points for winning
                print(f'Your current points: {player_points}')
            elif total == 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (It\'s a draw! Try again!)')
            else:
                print(
                    f'\nYou rolled: {rolled_numbers} (Sorry, you lose!)')
                player_points -= 3  # Deduct points for losing
                print(f'Your current points: {player_points}')
            print(f'Total score: {total}')
            roll_count += 1
            print(f'You have rolled the dice {roll_count} times. \n')
            if roll_count > 0:
                average_roll = total_roll_value // roll_count
                print(f'Average roll value: {average_roll:.2f}')
                print(f'Total doubles rolled: {total_doubles}')
                print(f'Highest roll: {highest_roll}')
                print(f'Lowest roll: {lowest_roll}\n')
        if mode_input == "lucky":
            if has_doubles:
                print(
                    f'\nYou rolled: {rolled_numbers} (Doubles! You get an extra turn!)')
                player_points += 10  # Award points for doubles
                print(f'Your current points: {player_points} \n')
                continue  # Allow the player to roll again immediately
            if total > 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
                player_points += 5  # Award points for winning
                print(f'Your current points: {player_points}')
            elif total == 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (It\'s a draw! Try again!)')
            else:
                print(
                    f'\nYou rolled: {rolled_numbers} (Sorry, you lose!)')
                player_points -= 3  # Deduct points for losing
                print(f'Your current points: {player_points}')
            print(f'Total score: {total}')
            roll_count += 1
            print(f'You have rolled the dice {roll_count} times. \n')
            if roll_count > 0:
                average_roll = total_roll_value // roll_count
                print(f'Average roll value: {average_roll:.2f}')
                print(f'Total doubles rolled: {total_doubles}')
                print(f'Highest roll: {highest_roll}')
                print(f'Lowest roll: {lowest_roll}\n')
        if mode_input == "risk":
            if total < 7:
                print(
                    f'\nYou rolled: {rolled_numbers} (Risky! You lose points!)')
                player_points -= 3  # Deduct points for risky roll
                print(f'Your current points: {player_points}')
            elif total > 10:
                print(
                    f'\nYou rolled: {rolled_numbers} (Congratulations! You win!)')
                player_points += 5  # Award points for winning
                print(f'Your current points: {player_points}')
            else:
                print(
                    f'\nYou rolled: {rolled_numbers} (It\'s a draw! Try again!)')
            print(f'Total score: {total}')
            roll_count += 1
            print(f'You have rolled the dice {roll_count} times. \n')
            if roll_count > 0:
                average_roll = total_roll_value // roll_count
                print(f'Average roll value: {average_roll:.2f}')
                print(f'Total doubles rolled: {total_doubles}')
                print(f'Highest roll: {highest_roll}')
                print(f'Lowest roll: {lowest_roll}\n')
    elif user_input == 'n':
        print('\nThank you for playing! Goodbye!')
        break
    else:
        print("\nInvalid input. Please enter 'y' or 'n'.\n")
