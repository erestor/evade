import numpy as np

# minimax for computer player, func called in computer_1
DEBUG_MODE = True

def evaluate_possition(move):   #move (only possible!) in format ((1, 2, (0, 2)), [0.0, (1, 2)]) (player, figure, coordinates)(situation on possible postiion, coordinates)
	value = 0 #expected range from 0 - 100
	player = (move[0])[0]
	#print("player", player)
	#print(((move[0])[2])[0])
	
	if player == 1:
		if (move[0])[1] == 2: #if figure to move is a KING
			if DEBUG_MODE:
				if ((move[1])[1])[0] == 3: #if possible move is winning move
					value = 100
				elif ((move[1])[1])[0] == 5:
					value = 100
			if ((move[0])[2])[0] < ((move[1])[1])[0]: #if current row is lesser than possible row (idea: for king is better to move to  row closer to the end)
				value =  60
			elif ((move[0])[2])[0] == ((move[1])[1])[0]: #if current row is equal to possible row (idea: for king better to go forward)
				value =  50
			else:
				value = 1
		else: # figure to move is a STONE
			if (move[1])[0] != 0: #better to freeze (i.e if value on possible spot is not = 0)
				value = 80
			elif ((move[0])[2])[0] < ((move[1])[1])[0]: #if current row is lesser than possible row (idea: for stone is better to move forward)
				value =  60
			else:
				value = 1
	else: #player == 2
		if (move[0])[1] == 9: #if figure to move is a KING
			if ((move[1])[1])[0] == 0:  #if possible move is not winning move
				value = 100
			elif ((move[0])[2])[0] > ((move[1])[1])[0]: #if current row is higher than possible row (idea: for king is better to move to  row closer to the end)
				value =  60
			elif ((move[0])[2])[0] == ((move[1])[1])[0]: #if current row is equal to possible row (idea: for king better to go forward)
				value =  50
			else:
				value = 1
		else: #figure is a STONE
			if (move[1])[0] != 0: #better to freeze (i.e if value on possible spot is not = 0)
				value = 80
			else:
				value = 1
	if DEBUG_MODE:	
		print("value", value)
	return value


#evaluate_possition(((1, 2, (0, 2)), [0.0, (1, 2)]))


def change_format_move(move): #take input (((1, 1, (0, 3)), [9.0, (1, 3)]) return for move_figure ([1, 2.0, (0, 2)], [1, 0.0, (0, 3)])
	#support funcion
	player = (move[0])[0]
	new_move_after = player, (move[1])[0], (move[1])[1]
	new_move = move[0], new_move_after
	#print(new_move_after)
	#print(new_move)
	return new_move

#change_format_move(((1, 1, (0, 3)), [9.0, (1, 3)]))


#[((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])]

def return_best_move(OK_moves): # [((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])] figure...possible moves, figure..possible moves
	#take a list of OK moves, evaluate them and select best move
	number_of_figures = len(OK_moves)
	value = 0
	best_move = 0
	print("number of figures", number_of_figures)
	for i in range(0, number_of_figures):
		number_of_moves_for_figure = len((OK_moves[i])[1])
		print("number_of_moves_for_figure", number_of_moves_for_figure)
		for j in range(0, number_of_moves_for_figure):
			move = (OK_moves[i])[0], ((OK_moves[i])[1])[j]
			actual_value = evaluate_possition(move)
			print(move, actual_value)
			if value < actual_value:
				value = actual_value
				modified_move = change_format_move(move)
				best_move = modified_move, actual_value

	print("highest value and move", best_move)
	return best_move

#return_best_move([((1, 2, (0, 2)), [[0.0, (1, 2)]]), ((1, 1, (0, 3)), [[0.0, (1, 2)], [9.0, (1, 3)]])])




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



