import numpy as np
import random

from P_board_1 import create_board
from P_board_1 import move_figure
from P_check_rules_1 import global_check_computer
from P_computerAI_1 import return_best_move
# computer player


DEBUG_MODE = True
TEST_MODE = False #test only commputer game itself




if TEST_MODE:
    temp_board = create_board()
    temp_board[1][1] = 5
    temp_board[1][0] = 5
    temp_board[2][2] = 2
    print("temp board")
    print(temp_board)

    player = 1 #info should be received once a player makes a choose at the beginning of game
    strength = 1 #dtto

####################################################
# useful functions
def car(cons):
    return cons[0]
def second_item(cons): #nejde o spravny cdr, psano pro ucelove
    return cons[1]
def cdr(cons):
    ic = 1
    cdr_list = []
    for ic in range (1, len(cons)):
        cdr_list.append(cons[ic])
        ic += 1
    return cdr_list
####################################3


def list_of_OK_moves(player, board):
    if player == 1:
        list_of_ALL_moves = global_check_computer(1, board) #reverse player because global_check controls the oponent status
    else:
        list_of_ALL_moves = global_check_computer(2, board)
    
    if list_of_ALL_moves == 0: #False:
        terminate = 0
        return terminate

    #return list on format [[[1.0, (0, 0)]], [[2.0, (0, 2)], [0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]]
    #                 [figure(position)][possible moves], ... possible moves inform about current figure on sport (not after move value)
    length_of_list = len(list_of_ALL_moves)

    if DEBUG_MODE:
        #print("list of ALL moves", list_of_ALL_moves)
        #print("length of list of all moves", length_of_list)
        print(" ")

    return list_of_ALL_moves #return False if is empty

#list_of_OK_moves(1, temp_board)

def random_AI_choice(player, board):
    # for random AI play, choice generated from list_of_ok_moves
    #new list in format [((2, 2, (0, 2)), [[2.0, (0, 2)], [0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]), ((2, 1, (2, 2)), [[0.0, (1, 2)], [0.0, (1, 3)], [0.0, (2, 1)], [1.0, (2, 2)], [0.0, (2, 3)], [0.0, (3, 2)]])]
    # ([figure][[moves][moves]]),([figure][[moves][moves]])
    
    input_list = list_of_OK_moves(player, board)
    if input_list == 0:
        terminate = 0
        return terminate

    print("lenght of input list", len(input_list))
    output_list = []
    for i in range (0, len(input_list)):
        figure_info = car(input_list[i])
        possibilities = cdr(input_list[i])
        info = figure_info, possibilities[0]

        if DEBUG_MODE:
            print("figure_info", figure_info)
            print("possibilities", possibilities[0])
            print("info", info)

        output_list.append(info) #[((2, 2, (0, 2)), [[0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]), ((2, 1, (2, 2)), [[0.0, (1, 2)], [0.0, (1, 3)], [0.0, (2, 1)], [0.0, (2, 3)], [0.0, (3, 2)]])]
                                #[((player(ignore), figure, (coordinates)), [[possible move] [possible move]]), ((another figure))...
    

    random_figure_index = random.randint(0, (len(output_list)) - 1)  #output_list
    moves_for_random_figure = output_list[random_figure_index] #([2.0, (0, 2)], [[0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]])
                                                                #position of figure + 3 possible moves
    
    mod_moves_list = cdr(moves_for_random_figure) #i.e [[[4.0, (7, 6)], [3.0, (5, 5)], [6.0, (9, 8)]]]
    
    selected_random_figure = player, car(moves_for_random_figure) #(1, [2.0, (0, 2)])
    number_of_choices = len(car(cdr(moves_for_random_figure)))
    random_choice_index = random.randint(0, (number_of_choices) - 1)
    random_selected_position = player, car(cdr(moves_for_random_figure))[random_choice_index] # (1, [0.0, (1, 3)])
    result = selected_random_figure, random_selected_position #((1, [2.0, (0, 2)]), (1, [0.0, (1, 3)]))

    if DEBUG_MODE:
        print("output list", output_list) #[([2.0, (0, 2)], [[0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]])]
        print("number of possible pigures", len(output_list))
        print("random_figure index", random_figure_index)
        print("selected_random_figure", selected_random_figure)
        print("moves_for_random_figure", moves_for_random_figure)
        print("mod_moves_list", mod_moves_list)
        print("number_of_choices", number_of_choices)
        print("random choice index", random_choice_index)
        print("random_selected_position", random_selected_position) 
        print("result", result)
    return result
    #result as random choice 0 and random coordinates [1, 0.0, (0, 3)]

#random_AI_choice([[[1.0, (0, 0)], [4.0, (7, 6)], [3.0, (5, 5)], [6.0, (9, 8)]], [[2.0, (0, 2)], [0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]])

#temp_input_list = [[[1.0, (0, 0)], [4.0, (7, 6)], [3.0, (5, 5)], [6.0, (9, 8)]], [[2.0, (0, 2)], [0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]]

def change_format_4_CPP(input):
    #support - to change wrong arrangement in array from ((1, (2, 1, (2, 2))), (1, [0.0, (1, 3)]))
    #                                       to (board,    [1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) for "move funciton"
    list_before_temp = ((input[0])[1])[1], ((input[0])[1])[2]

    player = (input[0])[0]
    fig_value = float(list_before_temp[0])
    list_before = [player, fig_value, list_before_temp[1]] # OK
    list_after = [player, ((input[1])[1])[0], ((input[1])[1])[1]]
    mod_list = list_before, list_after

    if DEBUG_MODE:
        print("list before temp", list_before_temp)
        #print("list befero [0] ", list_before_temp[1])
        print("list before", list_before)
        #list_after_temp = ((input[1])[1])[0], ((input[1])[1])[1]
        print("list after", list_after) #ok
        print("mod list in change format 4 CPP", mod_list)

    return mod_list



# MAIN function for respones AI to main ################ SIMPLIFY!
def call_computer_player(player, board, strength):
    if player == 1:
        print("computer play as player 1")
        if strength == 1:
            ai_raw_input = random_AI_choice(player, board) #((1, [2.0, (0, 2)]), (1, [0.0, (1, 3)]))
            if ai_raw_input == 0:
                print("Computer loose, no figure to move")
                return False 
            #list for move should be in format (board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) #player, figure, coordinates
            ai_input = change_format_4_CPP(ai_raw_input)
            if DEBUG_MODE:
                #print("ai raw input", ai_raw_input) #((1, [2.0, (0, 2)]), (1, [0.0, (1, 3)]))
                print("ai input", ai_input)
            
            move_figure(board, ai_input[0], ai_input[1]) #print should be move figure / figure and figure on sport 2.0 0.0
        elif strength == 2:
            OK_moves = list_of_OK_moves(player, board) #return format [((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])]
            print("OK_moves in C-player levl2", OK_moves)
            if OK_moves == 0:
                print("Computer loose, no figure to move")
                return False 
            best_move = return_best_move(OK_moves) #(((1, 1, (0, 3)), (1, 9.0, (1, 3))), 80)
            
            move_figure(board, (best_move[0])[0], (best_move[0])[1])
            #(board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)])
            #TBD
        else:
            print("AI TBD")
            #move_figure(board, return[0], return[1]) #return of mimimax called form computer_AI
            return False
    else: 
        print("computer play as player 2")
        if strength == 1:
            ai_raw_input = random_AI_choice(player, board) #((1, [2.0, (0, 2)]), (1, [0.0, (1, 3)]))
            ai_input = change_format_4_CPP(ai_raw_input)
            if DEBUG_MODE:
                print("ai raw input", ai_raw_input) #((1, [2.0, (0, 2)]), (1, [0.0, (1, 3)]))
                print("ai input", ai_input)
            move_figure(board, ai_input[0], ai_input[1]) #print should be move figure / figure and figure on sport 2.0 0.0
        elif strength == 2:
            OK_moves = list_of_OK_moves(player, board) #return format [((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])]
            print("OK_moves in C-player level 2:", OK_moves)
            if OK_moves == 0:
                print("Computer loose, no figure to move")
                return False 
            best_move = return_best_move(OK_moves) #(((1, 1, (0, 3)), (1, 9.0, (1, 3))), 80)
            
            move_figure(board, (best_move[0])[0], (best_move[0])[1])
        else:
            print("AI TBD")
            return False
    return True


