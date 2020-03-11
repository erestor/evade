from P_input_funcs_1 import ask_input
from p_init_game_1 import init_game
from P_player import PlayerColor
from P_board_1 import Board
from P_board_1 import Move
from P_board_1 import Coords

# The file is called only by "main" to deliver "get action"

from P_debug import DEBUG_MODE

counter = 0


#input qustions
q1 = "Select a figure on the ROW: "
q2 = "Select a figure on the COLUMN: "
q3 = "Move the figure on the ROW: "
q4 = "Move the figure on the COLUMN: "

def ask_input_source_move() -> Coords:
	x = ask_input(q1)
	y = ask_input(q2)
	return Coords(x, y)

def ask_input_target_move() -> Coords:
	x = ask_input(q3)
	y = ask_input(q4)
	return Coords(x, y)

def get_where_to_move(player_color: PlayerColor, board: Board) -> Move:
	while True:
		source = ask_input_move()
		if board.get(source).matches_player_color(player_color):
			break
		else:
			print("wrong move, try it again")

	while True:
		target = ask_input_move()
		move = Move(source, target);
		if board.is_possible_moves(move):
			break;
		else:
			print("wrong move, try it again")

	return move

#get_where_to_move(2)

def play_game(board: Board):
	turn = 0
	counter = 0
	players = init_game()
	print(' ')

	while True:
		if turn == 0:
			player_color = PlayerColor.white                
			opponent_has_valid_move = board.exists_valid_move(PlayerColor.black)
		else:
			player_color = PlayerColor.black
			opponent_has_valid_move = board.exists_valid_move(PlayerColor.white)

		if not opponent_has_valid_move: #win by oponent's inability to move
			print("Player " + player_color.name + " - you win")
			break #to finish the game

		print("Player: ", player_color, "it's your turn!") #check it !!!

		current_player = players[player_color.value]
		if current_player.is_computer():
			if not board.play(player_color, current_player.strength):
				break
		else:
			human_move = get_where_to_move(player_color)
			board.execute(human_move)

		turn += 1
		counter += 1
		print("counter", counter)
		turn = turn % 2

		if board.is_game_over():
			if board.white_won():
				print("Player " + PlayerColor.white.name + " - you win")
			elif board.black_won():
				print("Player " + PlayerColor.black.name + " - you win")
			else:
				print("Draw")

			break

#play_game()