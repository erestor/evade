from P_board_1 import Board
from P_play_game_1 import play_game
from P_debug import DEBUG_MODE

print("Hello Evade")
print("For help simply type 'help'")

#MAIN
def create_board():
	if DEBUG_MODE:
		return Board(4)

	return Board()

play_game(create_board())
                  
print("TBD aftergame menu")
print("END")
