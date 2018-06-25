'''
Rock-Spock-Paper-Lizard-Scissors
'''


import math
import random

def name_to_number(name):
    if name == "rock":
        number = 0
    elif name == "spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    else:
        number = 4
    return number


def number_to_name(number):
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    else:
        name = "scissors"
    return name
    

def rpsls(player_choice):
    print("Player chooses " + player_choice)
    player_number = name_to_number(player_choice)
    computer_number = random.randrange(0, 5)
    computer_choice = number_to_name(computer_number)
    print("Computer chooses " + computer_choice)
    difference = ((player_number - computer_number) % 5)

    if difference == 1 or difference == 2:
        print("Player wins!")
    elif difference == 3 or difference == 4:
        print("Computer wins!")
    else:
        print("Player and computer tie!")
    return ""

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
