import random

while True:
    user_input = input('Roll the dice? (y/n): ').lower()
    if user_input == 'y':
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        print(f'You rolled: {dice1} and {dice2}')
    elif user_input == 'n':
        print('Thank you for playing! Goodbye!')
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
