import numpy as np

# The file for managing a board

'''
Meaning of numbers in the game board
0 empty 
1 white stone
2 white king
8 black stone
9 black king
5 frozen position
'''


DEBUG_MODE = True

def create_board():
    # it creates a game board
    
    if DEBUG_MODE:
        # testing board
        board =  np.zeros((4, 4))
        board[0] = [0, 1, 0, 1]
        board[1] = [5, 5, 8, 5]
        board[2] = [5, 5, 5, 5]
        board[3] = [8, 0, 0, 5]


    else:
        # board according the rules
        board =  np.zeros((6, 6))
        board[0] = [1, 1, 2, 2, 1, 1] 
        board[5] = [8, 8, 9, 9, 8, 8]
    #print(board)

    return board

#board = create_board()

def move_figure (board, list_before, list_during): #list in format (board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) #player, figure, coordinates
    figure = list_before[1]
    figure_on_spot = list_during[1]
    if DEBUG_MODE:
        print("move figure / figure and figure on sport", figure, figure_on_spot)
    if figure_on_spot != 0:
        board[(list_during[2])[0]][(list_during[2])[1]] = 5
    else:
        board[(list_during[2])[0]][(list_during[2])[1]] = figure
    board[(list_before[2])[0]][(list_before[2])[1]] = 0
    
    print(' ')
    print("Board after the move")
    print(board)
    return board

def reverse_move_figure(board, list_before, list_during): #list in format (board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) #player, figure, coordinates
    figure = list_before[1]
    figure_on_spot = list_during[1]
    board[(list_during[2])[0]][(list_during[2])[1]] = figure_on_spot
    board[(list_before[2])[0]][(list_before[2])[1]] = figure
    print("board after reverse")
    print(board)
    return board