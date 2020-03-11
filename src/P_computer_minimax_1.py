import numpy as np

from P_computer_1 import list_of_OK_moves
from P_board_1 import create_board
from P_board_1 import move_figure
from P_board_1 import reverse_move_figure
from P_computerAI_1 import return_best_move
from P_computerAI_1 import evaluate_possition

#TEMPORARY
test_board = create_board()
#test_board[1] = 5
#test_board[1][1] = 5
#test_board[1][0] = 5
#test_board[2][2] = 2
print(test_board)


def make_tree(depth, player, board): # depth = number of cyclus before recursion
    first_list = list_of_OK_moves(player, board) #return format [((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])]
    print("first_list", first_list)
    number_of_figures = len(first_list)
    
    return_list = []
    max_return_list = []
    temporary_best_value = 0

    if player == 1:
        second_player = 2
    else:
        second_player = 1

    for i in range(0, number_of_figures): #for each figure
        number_of_moves_for_figure = len((first_list[i])[1])
        print("number_of_moves_for_figure [i]:", i, "is", number_of_moves_for_figure)
        for j in range(0, number_of_moves_for_figure):
            modify_move = ((first_list[i])[0])[0], (((first_list[i])[1])[j])[0], (((first_list[i])[1])[j])[1]
            move = (first_list[i])[0], modify_move
            print("move for fig [i]", i, "move option [j]", j, "move", move)
            
            move_4_eval = ((first_list[i])[0], ((first_list[i])[1])[j])
            value_rnd1 = evaluate_possition(move_4_eval)
            move_evaluated = move, value_rnd1
            print("move_evaluated", move_evaluated)

            move_figure(board, move[0], move[1]) #list in format (board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)])

            second_list = list_of_OK_moves(second_player, board)
            print("second_list for fig [i]move[j]", i, j, second_list)
            number_of_figures_P2 = len(second_list)

            for k in range(0, number_of_figures_P2):
                number_of_moves_for_figure_P2 = len((second_list[k])[1])
                print("number_of_moves_for_figure_P2 [k]:", k, "is", number_of_moves_for_figure_P2)
                for l in range(0, number_of_moves_for_figure_P2):
                    modify_move2 = ((second_list[k])[0])[0], (((second_list[k])[1])[l])[0], (((second_list[k])[1])[l])[1]
                    move2 = (second_list[k])[0], modify_move2
                    print("move for fig [k]", k, "move option [l]", l, "move2", move2)
                    move_figure(board, move2[0], move2[1]) 

                    move2_4_eval = ((second_list[k])[0], ((second_list[k])[1])[l])
                    value_rnd2 = - evaluate_possition(move2_4_eval) #reversed value from the first player point of view
                    move_evaluated2 = move2, value_rnd2

                    third_list = list_of_OK_moves(player, board)
                    print("third_list for fig [k]move[l]", k, l, third_list)
                    number_of_figures_P1_r2 = len(third_list)

                    for m in range(0, number_of_figures_P1_r2):
                        
                        number_of_moves_for_figure_P1_r2 = len((third_list[m])[1])
                        print("number_of_moves_for_figure_P1_r2 [m]:", m, "is", number_of_moves_for_figure_P1_r2)
                        eval_list_4_fig = [third_list[m]]
                        print("eval_list_4_fig", eval_list_4_fig)
                        best_move = return_best_move(eval_list_4_fig)
                        input_for_append = (move_evaluated, move_evaluated2, best_move, (i, j, k, l, m))
                        return_list.append(input_for_append)
                        print(" ")

                        
                        '''
                        if best_move[1] > temporary_best_value:
                            temporary_best_value = best_move[1]
                            input_for_append2 = (move, move2, best_move)
                            max_return_list.append(input_for_append2)
                        temporary_best_value = 0
                        '''
                    print("reverse depth 2")
                    reverse_move_figure(board, move2[0], move2[1])
            reverse_move_figure(board, move[0], move[1])
            print("return list")
            print(return_list)
            print(" ")
            for a in range(0, len(return_list)):
                print(return_list[a])

            

make_tree(2, 1, test_board)

#return_best_move([((1, 1, (0, 2)), [[0.0, (0, 1)], [0.0, (0, 3)]])])
#return_best_move([((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])])

'''

def make_tree(depth, player, board): # depth = number of cyclus before recursion
    first_list = list_of_OK_moves(player, board) #return format [((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])]
    number_of_figures = len(first_list)
    best_value = 0 #to select the best move
    if player == 1:
        second_player = 2
    else:
        second_player = 1
    #fake_board = board
    #list_of_moves_rnd1 = []

    for i in range(0, number_of_figures): #for each figure
        print("round i no ", i)
        number_of_moves_for_figure = len((first_list[i])[1])
        print("number_of_moves_for_figure", number_of_moves_for_figure)
        for j in range(0, number_of_moves_for_figure): # for each move for given figure
            print("round j no ", j)
            modify_move = ((first_list[i])[0])[0], (((first_list[i])[1])[j])[0], (((first_list[i])[1])[j])[1]
            move = (first_list[i])[0], modify_move
            print(move)
            move_figure(board, move[0], move[1]) #list in format (board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)])
            second_list = list_of_OK_moves(second_player, board) #[((2, 8, (3, 0)), [[0.0, (3, 1)]])] #create list of ok moves for second player (for each first player option)
            #print("second_list", second_list) 
            number_of_figures_player2 = len(second_list)
            for k in range (0, number_of_figures_player2): #figures which second player may use after specific move of white
                print("round k no ", k)
                number_of_moves_for_figure_player2 = len((second_list[k])[1])
                print("number_of_moves_for_figure_player2", number_of_moves_for_figure_player2)
                for l in range(0, number_of_moves_for_figure_player2): #moves for each second player's figure
                    print("round l no ", l)
                    modify_move2 = ((second_list[k])[0])[0], (((second_list[k])[1])[l])[0], (((second_list[k])[1])[l])[1]
                    move2 = (second_list[k])[0], modify_move2 #((2, 8, (3, 0)), (2, 0.0, (3, 1)))
                    print("move2", move2)
                    move_figure(board, move2[0], move2[1])

                    move_for_eval = (second_list[k])[0], ((((second_list[k])[1])[l])[0], (((second_list[k])[1])[l])[1])
                    print("move_for_eval", move_for_eval)
                    #temporary ...mayber wrong
                    value_of_move = evaluate_possition(move_for_eval) #input ((1, 2, (0, 2)), [0.0, (1, 2)])
                    print("possiblemove", move, move2, value_of_move )
                    #
                    if list_of_OK_moves(player, board) == 0:
                        print("early end of the tree")
                        transfer_list = move, move2, (((1, 0, (0, 0)), (1, 0.0, (0, 0))), 0)
                        break
                    third_list = list_of_OK_moves(player, board) # list for white after prevous move black after previous move white

                    possible_best_move = return_best_move(third_list) #(((1, 1, (0, 3)), (1, 9.0, (1, 3))), 80) #pick the best move for white at that level / i.e MAX
                    print("possible_best_move", possible_best_move)

                    value_of_possible_move = possible_best_move[1]
                    #print("temporary transfer list", move, move2, possible_best_move)

                    #nonsense...return_best_value already did this...if alwayse valid
                    if value_of_possible_move > best_value:
                        best_value = value_of_possible_move
                        transfer_list = move, move2, possible_best_move
                    #

                    reverse_move_figure(board, move[0], move[1]) #change board step back
            
            reverse_move_figure(board, move[0], move[1]) #change board back to original status
            print("transfer_list", transfer_list)

            #second_list = list_of_OK_moves(second_player, fake_board)
            #print("second_list", second_list)
            #fake_board = board
'''
