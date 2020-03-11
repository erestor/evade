import numpy as np 

import P_input_funcs_1
from P_input_funcs_1 import ask_type_of_player
from P_input_funcs_1 import select_computer_strength

DEBUG_MODE = False

def init_game():
    #ask player for choosing human/computer option 
    print("Lets begin the new game")
    print("Player 1 - Who are you?")
    Player_1 = ask_type_of_player()
    if Player_1 == 'C':
        computer_strength_p1 = select_computer_strength()
    else:
        computer_strength_p1 = '0'
    if DEBUG_MODE:
        print(Player_1, computer_strength_p1)
    print("Player 2 - Who are you?")
    Player_2 = ask_type_of_player()
    if Player_2 == 'C':
        computer_strength_p2 = select_computer_strength()
    else:
        computer_strength_p2 = '0'
    players_and_strength = [Player_1, computer_strength_p1, Player_2, computer_strength_p2]
    if DEBUG_MODE:
        print(players_and_strength)
    
    return players_and_strength