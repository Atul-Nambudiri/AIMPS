class Position(object):
	def __init__(self, pos, cost):
		self.pos = pos
		self.cost = cost
		return

	def __cmp__(self, other):
		return cmp(self.cost, other.cost)
