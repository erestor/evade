from P_debug import DEBUG_MODE
import numpy as np

'''
# TO DO
list_of_OK_moves(player,board) resuls as [((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])]
                                         figure, no move), [[figure, (move1, move2,...)
...create function evaluate(item, board) item as ([1, 2.0, (0, 2)], [1, 0.0, (0, 3)]), it returns number
evaluate item in list_o_ OK_moves in format - it returns (([1, 2.0, (0, 2)], [1, 0.0, (0, 3)], 322) / figure, intended position, value
create SUM ... list_evaluation in format (figure, new position, value), (figure, new position, value),..
                                        (([1, 2.0, (0, 2)], [1, 0.0, (0, 3)], 322), (another....))
parent == single item from list_evaluation in format               (([1, 2.0, (0, 2)], [1, 0.0, (0, 3)], 322)
...create a function for expecting_value_after_move ... it returns (([1, 2.0, (0, 2)], [1, 2.0, (0, 3)], 322) #change fig.value
for parent create temporary_board (with expected value) ...it returns temp_board and parent
> list_of_OK_moves for(OPPONENT_player, temporary_board) result as 
//// keep info about parents..append?
> evaluate item in list_of_OK_moves for OPPONENT with REVERSE value
> create a list_evaluation in format (item, temp_board) #
> create SUM ... list_evaluation
>> repeat x times
>> do minimax though evaluations... back to the top to select a move
>> return ([1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) #figure ..to move where


level 1 = random
level 2 = 3 cycles - white,black,white,black(end)
level 3 = 7 cycles ?
'''


######## MAIN #############
def minimax(player, board, strength):
    #result should be in format ([1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) for move_figure
                                #figure ..to move where
    pass


'''
https://www.youtube.com/watch?v=l-hh51ncgDI&t=320s

MINIMAX PSEUDOCODE from https://pastebin.com/VSehqDM3

function minimax(position, depth, maximizingPlayer)
	if depth == 0 or game over in position
		return static evaluation of position

	if maximizingPlayer
		maxEval = -infinity
		for each child of position
			eval = minimax(child, depth - 1, false)
			maxEval = max(maxEval, eval)
		return maxEval

	else
		minEval = +infinity
		for each child of position
			eval = minimax(child, depth - 1, true)
			minEval = min(minEval, eval)
		return minEval


// initial call
minimax(currentPosition, 3, true)
'''



