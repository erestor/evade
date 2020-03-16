from P_input_funcs_1 import ask_input
from p_init_game_1 import init_game
from P_player import PlayerColor
from P_board_1 import Board
from P_board_1 import Move
from P_board_1 import Coords

#input questions
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

def play_game(board: Board):
	players = init_game()
	player_color = PlayerColor.white
	counter = 0

	while True:
		counter += 1
		print("Move: " + str(counter))
		print("Player " + player_color.name + ": it's your turn!")
		current_player = players[player_color.value]
		if current_player.is_computer():
			board.play(player_color, current_player.strength)
		else:
			human_move = get_where_to_move(player_color)
			board.execute(human_move)

		if board.is_game_over():
			if board.is_draw():
				print("Draw")
			else:
				print("Player " + player_color.name + " - you win")

			break

		player_color = player_color.get_opposite()
		if not board.exists_valid_move(player_color): #the player who should continue cannot - opponent wins
			print("Player " + player_color.get_opposite().name + " - you win")
			break

#play_game()