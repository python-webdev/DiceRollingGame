# Loop inside:
#   Ask: roll the dice?
#   If user enters y
#     Generate two random numbers between 1 and 6
#     Print them
#   If user enters n
#     Print "Thank you for playing! Goodbye!"
#     Terminate the program
#   Else
#     Print "Invalid input. Please enter 'y' or 'n'."
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
