from P_debug import DEBUG_MODE
from P_player import PlayerColor
from P_cross import CrossState
from P_cross import Cross
from P_tree import calculate_value_by_minimax

from enum import Enum
from anytree import AnyNode
import random

# The file for managing a board

WINNING_MOVE_VALUE = 1000

class Coords:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def to_string(self) -> str:
		return '(' + str(self.x) + ',' + str(self.y) + ')'

class UndoInfo(Coords):
	def __init__(self, x, y, state: CrossState):
		super().__init__(x, y)
		self.state = state

class Move:
	def __init__(self, from_coords: Coords, to_coords: Coords):
		self.from_coords = from_coords
		self.to_coords = to_coords
		self.value = -100;

	def is_same_row(self) -> bool:
		return self.from_coords.x == self.to_coords.x

class Board:
	def __init__(self, size: int = 6):
		self.crosses = []
		self.columns = size
		for i in range(size * size):
			self.crosses.append(Cross(CrossState.empty))

		self.undo_stack = []

		if size == 4:
			# testing board
			self.__setRow(0, [CrossState.white_stone, CrossState.white_stone, CrossState.white_king, CrossState.white_stone])
			self.__setRow(3, [CrossState.black_stone, CrossState.black_king, CrossState.black_stone, CrossState.black_stone])
	
		else:
			# board according to the rules
			self.__setRow(0, [CrossState.white_stone, CrossState.white_stone, CrossState.white_king, CrossState.white_king, CrossState.white_stone, CrossState.white_stone])
			self.__setRow(5, [CrossState.black_stone, CrossState.black_stone, CrossState.black_king, CrossState.black_king, CrossState.black_stone, CrossState.black_stone])

	def get(self, coords: Coords) -> Cross:
		return self.__get(coords.x, coords.y)

	def set(self, coords: Coords, state: CrossState):
		self.undo_stack.append(UndoInfo(coords.x, coords.y, self.get(coords).state))
		self.__set(coords.x, coords.y, state)

	def is_empty(self, coords: Coords):
		return self.get(coords).is_empty()

	def execute(self, move: Move):
		#each move has two steps
		if self.is_empty(move.to_coords):
			self.set(move.to_coords, self.get(move.from_coords).state)
		else:
			self.set(move.to_coords, CrossState.frozen)

		self.set(move.from_coords, CrossState.empty)

	def undo_last_move(self):
		#each move has two undo steps
		first_half = self.undo_stack.pop()
		self.__set(first_half.x, first_half.y, first_half.state)
		second_half = self.undo_stack.pop()
		self.__set(second_half.x, second_half.y, second_half.state)

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

	def evaluate_move(self, move: Move):
		source_figure = self.get(move.from_coords)
		target_figure = self.get(move.to_coords)
		value = -5
		if source_figure.is_king():
			if self.is_win_destination(source_figure, move.to_coords.x):
				value = WINNING_MOVE_VALUE
			elif self.is_move_forward(source_figure, move):
				value = 20
			elif move.is_same_row():
				value = 5
		else:
			if self.is_freezing_move(source_figure, target_figure):
				if target_figure.is_king():
					value = 80
				else:
					value = 30
			elif self.is_move_forward(source_figure, move):
				value = 10
			elif move.is_same_row():
				value = 0

		move.value = value

	def get_best_move(self, ok_moves: list) -> Move:
		best_move = Move(0, 0)
		for move in ok_moves:
			self.evaluate_move(move)
			if move.value > best_move.value:
				best_move = move

		return best_move

	def get_best_move_minimax(self, player_color: PlayerColor) -> Move:
		root = AnyNode(id = 'Root', level = 1)
		self.build_move_tree(root, player_color, max_depth = 4)

		#we have the move tree with evaluated leaves, now calculate all nodes
		root.value = calculate_value_by_minimax(root)

		#get moves with best value, which is the value of the root node
		best_moves = []
		for node in root.children:
			if node.value == root.value:
				best_moves.append(node.data)

		return best_moves[random.randint(0, len(best_moves) - 1)]

	def build_move_tree(self, node: AnyNode, next_player_color: PlayerColor, max_depth: int):
		is_root = node.level == 1; #root node with level 1 represents null move which cannot be executed or evaluated
		opponent_turn = node.level % 2 == 1
		if not is_root:
			self.evaluate_move(node.data)
			if node.level == max_depth or node.data.value == WINNING_MOVE_VALUE:
				#we've reached a leaf in our tree, assign node value and finish recursion
				node.value = -node.data.value if opponent_turn else node.data.value
				return

			self.execute(node.data)

		next_moves = self.get_all_possible_moves(next_player_color)
		if len(next_moves) == 0:
			#the next player cannot move, hence this node is a winning node
			node.value = -WINNING_MOVE_VALUE if opponent_turn else WINNING_MOVE_VALUE
		else:
			for next_move in next_moves:
				next_move_node = AnyNode(parent = node, data = next_move, level = node.level + 1)
				self.build_move_tree(next_move_node, next_player_color.get_opposite(), max_depth)

		if not is_root:
			self.undo_last_move()

	def play(self, player_color: PlayerColor, strength) -> bool:
		if strength > 2:
			move_to_execute = self.get_best_move_minimax(player_color)
		else:
			ok_moves = self.get_all_possible_moves(player_color)
			if strength == 1:
				move_to_execute = ok_moves[random.randint(0, len(ok_moves) - 1)]
			else:
				move_to_execute = self.get_best_move(ok_moves)

		src = self.get(move_to_execute.from_coords).state
		self.execute(move_to_execute) #saves undo
		dst = self.get(move_to_execute.to_coords).state
		self.undo_stack = [] #but we don't need it

		print(player_color.name + ' played ' + src.name + move_to_execute.from_coords.to_string() + '->' + move_to_execute.to_coords.to_string() + dst.name)
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

	def __get(self, x, y) -> Cross:
		return self.crosses[x * self.columns + y]

	def __set(self, x, y, state: CrossState):
		self.crosses[x * self.columns + y].set(state)

	def __setRow(self, x, states: list):
		for y in range(len(states)):
			self.__set(x, y, states[y])
