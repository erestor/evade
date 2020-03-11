from P_debug import DEBUG_MODE
import enum
import numpy as np

import P_board_1
from P_board_1 import Board
from P_player import Player
from P_player import PlayerColor

'''
import P_play_game_1
from P_play_game_1 import send_actual_board
'''
# to check the rules before/after a move
# The file is called only by Play_game

'''
class MoveCheckResult(enum.Enum):
    FORBIDDEN_MOVE = 500
    OK_MOVE = 100
    FROZEN_MOVE = 200

#control_value2 = MoveCheckResult.OK_MOVE
'''

def check_figure(list): #list in format [(1, 1.0, (0, 0))] i.e. [player, figure (row, column)]
    list = list[0]
    figure = int(list[1])
    player = list[0]

    if figure == 0 or figure == 5:
        print("Forbidden position")
        return False #forbidden move
    elif player == 1:
        if figure == 8 or figure == 9:
            print("Forbidden position")
            return False #forbidden move
    elif player == 2:
        if figure == 1 or figure == 2:
            print("Forbidden position")
            return False #forbidden move
    if DEBUG_MODE:
        print("check_figure - control ok")
    return True #ok move

#print(check_figure([1, 5.0, (0, 0)]))

def is_valid_position(row, column):
    #serve for check if considered position is not outside the board, used in is_move_exists
    if DEBUG_MODE:
        if 0 <= row <= 3:
            if 0 <= column <= 3:
                return 100
    else:
        if 0 <= row <= 5:
            if 0 <= column <= 5:
                return 100
    return 500

def is_valid_move(player, tested_figure, possible_figure):
    if DEBUG_MODE:
        pass
        #print("received inputs for is valid move", player, tested_figure, possible_figure)
    if player == 1:
        if possible_figure == 5 or possible_figure == 1 or possible_figure == 2: #play on frozen or own stones
            return False
        elif tested_figure == 2: #king is not allowed to freeze
            if possible_figure != 0:
                return False
    elif player == 2:
        if possible_figure == 5 or possible_figure == 8 or possible_figure == 9: #play on frozen or own stones
            return False
        elif tested_figure == 9: #king is not allowed to freeze
            if possible_figure != 0:
                return False
    return True


def is_move_exists(list, board): #list in format [(1, 1.0, (0, 0))] i.e. [player, figure (row, column)]
    #check what are possible moves for selected figure, which is approved for moving from "check_figure"
    list_is = list [0]
    coordinates = list_is[2]

    i = -1
    j = -1

    tested_row = coordinates[0]
    tested_column = coordinates[1]
    tested_figure = list_is[1]
    player = list_is[0]
    list_of_possible_moves = []

    for i in range (-1, 2): #+/-1 row
        for j in range (-1, 2): #+/- column
            if is_valid_position(tested_row + i, tested_column + j) != 500: #position is inside the board
                if tested_row == tested_row + i and tested_column == tested_column + j:
                    pass
                else: #tested_row != 100: #tested_row + i != tested_row and tested_column + j != tested_column: #exclude own position i.e. no move ..WRONG
                    possible_figure = board[tested_row + i][tested_column + j]
                    #print("send to is valid move", player, tested_figure, possible_figure)
                    if is_valid_move(player, tested_figure, possible_figure):
                        valid_coordinates = [possible_figure, (tested_row + i, tested_column + j)]
                        list_of_possible_moves.append(valid_coordinates)
    
    result = list_is, list_of_possible_moves                   
    if DEBUG_MODE:
        #print("input list for is_move_exists", list_is)
        print("list of possible moves from is_move_exists - result", result)
    return result #list_of_possible_moves


def list_of_possible_coordinates(list): # list in format [(1, 2.0, (0, 2)), [[0.0, (0, 3)], [0.0, (1, 2)], [0.0, (1, 3)]]]
    #is a support for check if the move required by player possible. It uses already existing list of possible moves from "is_move_exists"
    input = list[1]
    #print("input for list of possible coordinates", input)
    list_of_coordinates = []
    for i in range (0, len(input)):
        coordinates = (input[i])[1]
        list_of_coordinates.append(coordinates)
        #print(list_of_coordinates)
    return list_of_coordinates

def check_move(list, intended_move): #list in format [(0, 3), (1, 2), (1, 3)]
    #now problem incoming list [(2, 8.0, (3, 0)), ((2, 8.0, (3, 0)), [[0.0, (2, 0)], [0.0, (2, 1)]])]
    list_input = list[1]
    check_list = list_of_possible_coordinates(list_input)
    if DEBUG_MODE:
        print("list", list)
        print("check list", check_list)
        print("intended move", intended_move)
    for i in range (0, len(check_list)):
        if check_list[i] == intended_move:
            return True
    else:
        return False


def check_end_game(player, board):
    if DEBUG_MODE:
        if np.any(board[3] == 2):
            print("White WINS!")
            return True
        elif np.any(board[0] == 9):
            print("Black WINS!")
            return True
        else:
            if np.any(board) == 2:
                if np.any(board) == 9:
                    pass
                else:
                    print("It is DRAW!")
                    return True
    else:
        #king in the last line
        if np.any(board[5] == 2):
            print("White WINS!")
            return True
        elif np.any(board[0] == 9):
            print("Black WINS!")
            return True
        #both kings frozen
        else:
            if np.any(board) == 2:
                if np.any(board) == 9:
                    pass
                else:
                    print("It is DRAW!")
                    return True
    return False


#def global_check(player: PlayerColor, board: Board):
#    #to check if there is a possibility to move with any figure for a player on move
    
#    total_list = []
#    for k in range (0, board.size):
#        for l in range (0, board.size):
#            figure = board.get(Coords(k, l))
#            if player == PlayerColor.white:
#                if figure.is_black():

#                    list_moves = [(player, figure, (k , l))] #[(1, 1.0, (0, 0))]
#                    #print("figure in global check", list_moves)

#                    possible_list = is_move_exists(list_moves, board) #([(1, 2.0, (2, 2))], [[0.0, (1, 2)], [0.0, (1, 3)], [0.0, (2, 1)], [0.0, (2, 3)], [0.0, (3, 2)]])

#                    #print("possible list in global check", possible_list)
#                    if len((possible_list)[1]) > 0:
#                        total_list.append(possible_list)
#            else:
#                player == 2
#                if figure == 1 or figure == 2:

#                    list_moves = [(player, figure, (k , l))] #[(1, 1.0, (0, 0))]
#                    #print("figure in global check", list_moves)
#                    possible_list = is_move_exists(list_moves, board) #([(1, 2.0, (2, 2))], [[0.0, (1, 2)], [0.0, (1, 3)], [0.0, (2, 1)], [0.0, (2, 3)], [0.0, (3, 2)]])                   
#                    #print("possible list in global check", possible_list)

#                    if len((possible_list)[1]) > 0: #was 0...why dif from player 1  ??????????
#                        total_list.append(possible_list)

#    if DEBUG_MODE:
#        print("global_check output /number of figures which can move ", len(total_list))

#    if len(total_list) == 0: ###################### fix it
#        print("empty total list")
#        return False
#    if DEBUG_MODE:
#        print("total list", total_list)
#    return total_list 

#############################################
# COMPUTER
def global_check_computer(player, board):
    #to check if there is a possibility to move with any figure for a player on move
    #duplicate/similar code as in check_rules
    #problem with switching player for global check and generating list of possible moves for computer when playing
    
    total_list = []
    if DEBUG_MODE:
        x = 4 #for smaller size of board
    else:
        x = 6

    for k in range (0, x):
        for l in range (0, x):
            figure = int(board[k][l])
            if player == 2:
                if figure == 8 or figure == 9:

                    list_moves = [(player, figure, (k , l))] #[(1, 1.0, (0, 0))]
                    #print("figure in global check", list_moves)
                    possible_list = is_move_exists(list_moves, board) #([(1, 2.0, (2, 2))], [[0.0, (1, 2)], [0.0, (1, 3)], [0.0, (2, 1)], [0.0, (2, 3)], [0.0, (3, 2)]])
                    #print("possible list in global check", possible_list)
                    if len((possible_list)[1]) > 0:
                        total_list.append(possible_list)
            else:
                player == 1
                if figure == 1 or figure == 2:

                    list_moves = [(player, figure, (k , l))] #[(1, 1.0, (0, 0))]
                    #print("figure in global check", list_moves)
                    possible_list = is_move_exists(list_moves, board) #([(1, 2.0, (2, 2))], [[0.0, (1, 2)], [0.0, (1, 3)], [0.0, (2, 1)], [0.0, (2, 3)], [0.0, (3, 2)]])                   
                    #print("possible list in global check", possible_list)

                    if len((possible_list)[1]) > 0: #was 1
                        total_list.append(possible_list)

    if DEBUG_MODE:
        print("global_check output /number of figures which can move ", len(total_list))

    if len(total_list) == 0: 
        print("empty total list")
        return 0 #False
    if DEBUG_MODE:
        print("total list", total_list)
    return total_list #orig.value = False, for computer player tested total_list
    ######################################################################################