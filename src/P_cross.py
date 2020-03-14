from enum import Enum
from P_player import PlayerColor

class CrossState(Enum):
	empty = 0
	white_stone = 1
	white_king = 2
	black_stone = 8
	black_king = 9
	frozen = 5

class Cross:
	def __init__(self, initalState: CrossState):
		self.state = initalState

	def set(self, state: CrossState):
		self.state = state

	def is_empty(self) -> bool:
		return self.state == CrossState.empty

	def is_frozen(self) -> bool:
		return self.state == CrossState.frozen

	def is_black(self) -> bool:
		return self.state == CrossState.black_king or self.state == CrossState.black_stone

	def is_white(self) -> bool:
		return self.state == CrossState.white_king or self.state == CrossState.white_stone

	def is_king(self) -> bool:
		return self.state == CrossState.white_king or self.state == CrossState.black_king

	def matches_player_color(self, color: PlayerColor) -> bool:
		if (color == PlayerColor.white and self.is_white()):
			return True
		elif (color == PlayerColor.black and self.is_black()):
			return True

		return False
