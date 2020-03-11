https://pypi.org/project/anytree/

from anytree import Node, RenderTree
from P_board_1 import Board

def make_root(player_color, board: Board) -> Node:
	root = Node('Root')
	ok_moves = board.get_all_possible_moves(player_color)
	for move in ok_moves:
		move_node = Node(move, root)

	return root

def make_tree(player_color, board: Board, parent: Node):
	board.execute(parent)
	ok_moves = board.get_all_possible_moves(player_color)
	for move in ok_moves:
		move_node = Node(move, parent)

	for child in parent.children
		board.evaluate_move(child.data)


#udo = Node('Udo")
#marc = Node("Marc", parent=udo)
#lian = Node("Lian", parent=marc)
#dan = Node("Dan", parent=udo)
#jet = Node("Jet", parent=dan)
#jan = Node("Jan", parent=dan)
#joe = Node("Joe", parent=dan)

#print(udo)
#Node('/Udo')
#print(joe)
#Node('/Udo/Dan/Joe')

#for pre, fill, node in RenderTree(udo):
#    print("%s%s" % (pre, node.name))