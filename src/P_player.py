from enum import Enum

class PlayerColor(Enum):
	white = 0
	black = 1

	def get_opposite(self):
		if self == PlayerColor.white:
			return PlayerColor.black
		return PlayerColor.white

class Player:
	def __init__(self, who, strength):
		self.who = who
		self.strength = strength

	def is_computer(self):
		return self.who == 'C'