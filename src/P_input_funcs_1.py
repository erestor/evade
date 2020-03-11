# all function asking user for input from keybord
# The file is called by init_game and play_game

from P_debug import DEBUG_MODE

def ask_type_of_player():
    #to choose a type of player, human or computer
    while True:
        player_type = input("Select a type of player: for Computer player press 'C', for Human player press 'H' ")
        if player_type.capitalize() == 'H' or player_type.capitalize() == 'C':
            return player_type.capitalize()
        else:
            print("wrong input")


def select_computer_strength():
    # to choose a strength of computer player
    strength_choices = [1, 2, 3]
    while True:
        computer_strength = input("How strong should the computer player be? Press '1' for weak, '2' for normal and '3' for strong: ")
        try:
            value = int(computer_strength)
            if value in strength_choices:
                return value
            else:
                print("wrong input")
        except ValueError:
            print("Error - wrong input")

def ask_input(w):
    #it ask for user's input and check its validity
    if DEBUG_MODE:
        numbers = [0, 1, 2, 3] #valid inputs in simplified conditions
    else:
        numbers = [0, 1, 2, 3, 4, 5] #valid inputs according rules
    correct = False
    while not correct:
        guess = input(w)
        if guess == 'help':
            make_help_menu()
        elif guess == 'board':
            print("board")
        elif guess == 'undo':
            print("TBD undo...")
        else:
            try:
                val = int(guess)
                if val in numbers:
                    correct = True
                    return val
                else:
                    print("no")
            except ValueError:
                print("error")


def make_help_menu():
    #to make a help menu in terminal 

    #INCOMPLETE!!!!!
    print("for move suggestions press 'M' ")
    print("for seeing rules of the Evade press 'E' ")
    print("for return to the game press 'R' ")
    print("for restart the game press 'X'")
    
    correct = False
    while not correct:
        answer = input("Enter your choice: ")
        if answer == 'E' or answer == 'M' or answer == 'R':
            correct = True

    if answer == 'E':
        print("TBD resume of Evades Rules... ")
    elif answer == 'M':
        print("TBD move suggestions...")
    elif answer == 'X':
        print("TBD restart the game...")
    else:
        print("Back to the game...")
