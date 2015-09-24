class PositionPlusGhost(object):
	"""
	A Position object that is used by the priority queue to get the position with the greatest priority, or low cost
	The object has two additional 
	"""

	def __init__(self, pos, ghost_pos, ghost_dir, cost):
		self.pos = pos
		self.cost = cost
		self.ghost_dir = ghost_dir
		self.ghost_pos = ghost_pos
		return

	def __cmp__(self, other):
		"""
		Implement the comparison function for the Position object
		"""
		return cmp(self.cost, other.cost)
