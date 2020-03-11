import numpy as np

import P_input_funcs_1
import P_check_rules_1
import P_board_1
import P_computer_1

from P_input_funcs_1 import ask_input

from P_board_1 import move_figure

from P_check_rules_1 import global_check
from P_check_rules_1 import check_figure
from P_check_rules_1 import check_figure
from P_check_rules_1 import is_move_exists
from P_check_rules_1 import check_move
from P_check_rules_1 import check_end_game


from P_board_1 import create_board

from p_init_game_1 import init_game

from P_computer_1 import call_computer_player

# The file is called only by "main" to deliver "get action"

DEBUG_MODE = False
counter = 0

board = create_board()
print("board created")
print(board)


#input qustions
q1 = "Select a figure on the ROW: "
q2 = "Select a figure on the COLUMN: "
q3 = "Move the figure on the ROW: "
q4 = "Move the figure on the COLUMN: "

def get_which_figure(player):
    # it call input functions and check rules functions. If valid if accept player's choice
    
    control_status = False

    while not control_status:
        
        selected_figure_row_l = ask_input(q1)
        selected_figure_col_l = ask_input(q2)

        figure = board[selected_figure_row_l][selected_figure_col_l]
        coordinates = (selected_figure_row_l, selected_figure_col_l)
        list_control = [(player, figure, coordinates)]
        #list_control = [(figure, coordinates)]
        if DEBUG_MODE:
            print("list as from get_which_player for is_move_exists", list_control)
        #list.append(coordinates)
        #print("list - user's input / before check", list)
        # CHECKs
        #control_1 = check_figure(list) #is it player's figure?
        
        if check_figure(list_control):
            list_is_move_exists = is_move_exists(list_control, board)
            if len(list_is_move_exists) != 0:
                list_control.append(list_is_move_exists)
                control_status = True
                #print("control_status", control_status)
            else:
                print("there is no move for the selected figure")

    
    if DEBUG_MODE:
        print("list - selected possible position", list_control)
    return (list_control)
     
#get_which_figure(2)


def get_where_to_move(player):

    control_status = False

    while not control_status:
        list_GWF = get_which_figure(player) #list in format [1, 2.0, (0, 2), [[0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]] where
                                        # [0-2] is initial position and [3] is a sub list of possible moves and stones on that position before move
        list_from = list_GWF[0] 
        selected_move_row_l = ask_input(q3)
        selected_move_col_l = ask_input(q4)

        figure = board[selected_move_row_l][selected_move_col_l]
        coordinates = (selected_move_row_l, selected_move_col_l)
        #print(coordinates)

        # CHECKS
        if check_move(list_GWF, coordinates):
            list_during_move = [player, figure, coordinates] #for UNDO later
            if DEBUG_MODE:
                print("list during move", list_during_move)
            move_figure(board, list_from, list_during_move)
            control_status = True
        else:
            print("wrong move, try it again")
        
    return board

#get_where_to_move(2)


def get_action(turn):
    end_game = False
    counter = 0

    players_and_strength = init_game() #list in form ['H', '0', 'C', 1]
    print(' ')

    while not end_game:
        if turn == 0:
            player = 1
            print("player", player)
            if not global_check(player, board): #win by oponent's inability to move
                print("Player 1 - you win //global_check")
                break #to finish the game
                
        else:
            player = 2
            print("player", player)
            if not global_check(player, board):
                print("Player 2 - you win //global_check")
                break
                
        print("Player: ", player, "it's your turn!") #check it !!!

        
        if player == 1 and players_and_strength[0] == 'C':
            if not call_computer_player(player, board, players_and_strength[1]):# call AI to play
                end_game = True 
        elif player == 2 and players_and_strength[2] == 'C':
            if not call_computer_player(player, board, players_and_strength[3]):
                end_game = True
        else:
            get_where_to_move(player)
        
        if check_end_game(player, board):
            end_game = True
        
        turn += 1
        counter += 1
        print("counter", counter)
        turn = turn % 2

    return True


#get_action(1)