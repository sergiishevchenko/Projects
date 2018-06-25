import math
import random
import simplegui

num_range = 100
guesses_remaining = 0
secret_number = 0

def new_game():
    global num_range, guesses_remaining, secret_number
    guesses_remaining = int(math.ceil(math.log((num_range - 0), 2)))
    secret_number = random.randrange(0, num_range)
    print("\nNew game. Range is from 0 to", num_range)
    print("Number of remaining guesses is", guesses_remaining)

def range100():
    global num_range
    num_range = 100
    new_game()

def range1000():     
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    global guesses_remaining
    print("\nGuess was", guess)
    guess = int(guess)
    guesses_remaining -= 1
    print("Number of remaining guesses is", guesses_remaining)
    if guesses_remaining > 0:
        if guess > secret_number:
            print("Lower")
        elif guess < secret_number:
            print("Higher")
        else:
            print("Correct")
            new_game()
    else:
        if guess == secret_number:
            print("Correct")
        else:
            print("You ran out of guesses. The number was", secret_number)
        new_game()
    
frame = simplegui.create_frame("Guess the number", 200, 200)

frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess:", input_guess, 200)
 
new_game()
