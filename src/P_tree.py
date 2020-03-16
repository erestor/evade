from anytree import AnyNode

def calculate_value_by_minimax(node: AnyNode):
	if len(node.children) == 0:
		return node.value
	else:
		#calculate and choose the appropriate child value
		for child in node.children:
			child.value = calculate_value_by_minimax(child)

		child_values = list(map(lambda x: x.value, node.children))

		#application of minimax
		if node.level % 2 == 0: #children are opponent moves
			return min(child_values)
		else:
			return max(child_values)
