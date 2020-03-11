from P_debug import DEBUG_MODE
import random

from enum import Enum
from P_player import PlayerColor
from P_cross import CrossState
from P_cross import Cross

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

class Coords:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

class Move:
	def __init__(self, from_coords: Coords, to_coords: Coords):
		self.from_coords = from_coords
		self.to_coords = to_coords

	def is_same_row(self) -> bool:
		return self.from_coords.x == self.to_coords.x

class Board:
	def __init__(self, size: int = 6):
		self.crosses = []
		self.columns = size
		for i in range(size * size):
			self.crosses.append(Cross(CrossState.empty))

		if size == 4:
			# testing board
			self.__setRow(0, [CrossState.empty, CrossState.white_stone, CrossState.empty, CrossState.white_stone])
			self.__setRow(1, [CrossState.frozen, CrossState.frozen, CrossState.black_stone, CrossState.frozen])
			self.__setRow(2, [CrossState.frozen, CrossState.frozen, CrossState.frozen, CrossState.frozen])
			self.__setRow(3, [CrossState.black_stone, CrossState.empty, CrossState.empty, CrossState.frozen])
	
		else:
			# board according the rules
			self.__setRow(0, [CrossState.white_stone, CrossState.white_stone, CrossState.white_king, CrossState.white_king, CrossState.white_stone, CrossState.white_stone])
			self.__setRow(5, [CrossState.black_stone, CrossState.black_stone, CrossState.black_king, CrossState.black_king, CrossState.black_stone, CrossState.black_stone])

	def get(self, coords: Coords) -> Cross:
		return self.__get(coords.x, coords.y)

	def set(self, coords: Coords, state: CrossState):
		self.__set(coords.x, coords.y, state)

	def is_empty(self, coords: Coords):
		return self.get(coords).is_empty()

	def execute(self, move: Move):
		if self.is_empty(move.to_coords):
			self.set(move.to_coords, self.get(move.from_coords).state)
		else:
			self.set(move.to_coords, CrossState.frozen)

		self.set(move.from_coords, CrossState.empty)

	def is_possible_move(self, from_coords: Coords, to_coords: Coords) -> bool:
		moving_figure = self.get(from_coords)
		target_figure = self.get(to_coords)
		if target_figure.is_empty():
			return True
		elif target_figure.is_white():
			if moving_figure.is_white():
				return False
			elif moving_figure.state == CrossState.black_king:
				return False
			elif moving_figure.state == CrossState.black_stone:
				return True
		elif target_figure.is_black():
			if moving_figure.is_black():
				return False
			elif moving_figure.state == CrossState.white_king:
				return False
			elif moving_figure.state == CrossState.white_stone:
				return True
		else:
			return False

	def is_valid(self, coords: Coords) -> bool:
		return coords.x >= 0 and coords.x < self.columns and coords.y >= 0 and coords.y < self.columns

	def get_possible_moves(self, source: Coords) -> list:
		result = []
		for delta_x in [-1, 0, 1]:
			for delta_y in [-1, 0, 1]:
				if delta_x == 0 and delta_y == 0:
					pass
				else:
					target = Coords(source.x + delta_x, source.y + delta_y)
					if self.is_valid(target) and self.is_possible_move(source, target):
						result.append(Move(source, target))

		return result;

	def get_all_possible_moves(self, player_color: PlayerColor) -> list:
		total_list = []
		for k in range (0, self.columns):
			for l in range (0, self.columns):
				coords = Coords(k, l)
				figure = self.get(coords)
				possible_list = []
				if figure.matches_player_color(player_color):
					possible_list = self.get_possible_moves(coords);

				total_list = total_list + possible_list

		print('get_all_possible_moves returns ', len(total_list), ' ', player_color.name)
		return total_list

	def exists_valid_move(self, player_color: PlayerColor) -> bool:
		return len(self.get_all_possible_moves(player_color)) > 0

	def is_win_destination(self, cross: Cross, x: int) -> bool:
		if cross.is_white():
			return x == self.columns - 1
		else:
			return x == 0 

	def is_move_forward(self, cross: Cross, move: Move) -> bool:
		if cross.is_white():
			return move.from_coords.x < move.to_coords.x
		else:
			return move.from_coords.x > move.to_coords.x

	def is_freezing_move(self, source: Cross, target: Cross) -> bool:
		if source.is_white():
			return target.is_black()
		else:
			return target.is_white()

	def evaluate_move(self, move: Move) -> int:
		source_figure = self.get(move.from_coords)
		target_figure = self.get(move.to_coords)
		if source_figure.is_king():
			if self.is_win_destination(source_figure, move.to_coords.x):
				return 100
			elif self.is_move_forward(source_figure, move):
				return 60
			elif move.is_same_row():
				return 50
		else:
			if self.is_freezing_move(source_figure, target_figure):
				return 80
			elif self.is_move_forward(source_figure, move):
				return 60

		return 1

	def get_best_move(self, ok_moves: list) -> Move:
		#take a list of OK moves, evaluate them and select best move
		best_value = 0
		best_move = Move(0, 0)
		for move in ok_moves:
			if self.evaluate_move(move) > best_value:
				best_move = move

		return move

	def play(self, player_color: PlayerColor, strength) -> bool:
		ok_moves = self.get_all_possible_moves(player_color)
		if strength == 1:
			move_to_execute = ok_moves[random.randint(0, len(ok_moves) - 1)]
		elif strength == 2:
			move_to_execute = self.get_best_move(ok_moves)
		else:
			print("AI TBD")
			#move_figure(board, return[0], return[1]) #return of mimimax called form computer_AI
			return False

		self.execute(move_to_execute)
		return True

	def is_game_over(self) -> bool:
		return self.white_won() or self.black_won() or self.is_draw()

	def white_won(self) -> bool:
		result = False
		for y in range(self.columns):
			figure = self.__get(self.columns - 1, y)
			if figure.is_white() and figure.is_king():
				result = True

		return result;

	def black_won(self) -> bool:
		result = False
		for y in range(self.columns):
			figure = self.__get(0, y)
			if figure.is_black() and figure.is_king():
				result = True

		return result;

	def has_king(self) -> bool:
		has_king = False
		for x in range(self.columns):
			for y in range(self.columns):
				figure = self.__get(x, y)
				if figure.is_king():
					has_king = True

		return has_king;

	def is_draw(self) -> bool:
		return not self.has_king()

	#private

	def __get(self, x, y):
		return self.crosses[x * self.columns + y]

	def __set(self, x, y, state: CrossState):
		self.crosses[x * self.columns + y].set(state)

	def __setRow(self, x, states: list):
		for y in range(len(states)):
			self.__set(x, y, states[y])


def reverse_move_figure(board, list_before, list_during): #list in format (board, [1, 2.0, (0, 2)], [1, 0.0, (0, 3)]) #player, figure, coordinates
    figure = list_before[1]
    figure_on_spot = list_during[1]
    board[(list_during[2])[0]][(list_during[2])[1]] = figure_on_spot
    board[(list_before[2])[0]][(list_before[2])[1]] = figure
    print("board after reverse")
    print(board)
    return board
