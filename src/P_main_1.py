
#import p_init_game_1
import P_play_game_1
import P_board_1

#from p_init_game_1 import init_game
from P_play_game_1 import get_action

print("Hello Evade")
print("For help simply type 'help'")


# Global variables

GAME_OVER = False
turn = 0 #who is on move, later set based on player's' choice

#MAIN
while not GAME_OVER:
        
    if get_action(turn): #file: play_game
        GAME_OVER = True
                  
print("TBD aftergame menu")
print("END")


