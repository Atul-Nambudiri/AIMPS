class Position(object):
	"""
	A Position object that is used by the priority queue to get the position with the greatest priority, or low cost
	"""
	
	def __init__(self, pos, cost):
		self.pos = pos
		self.cost = cost
		return

	def __cmp__(self, other):
		"""
		Implement the comparison function for the Position object
		"""
		return cmp(self.cost, other.cost)
