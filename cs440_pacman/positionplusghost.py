class PositionPlusGhost(object):
	def __init__(self, pos, ghost_pos, ghost_dir, cost):
		self.pos = pos
		self.cost = cost
		self.ghost_dir = ghost_dir
		self.ghost_pos = ghost_pos
		return

	def __cmp__(self, other):
		return cmp(self.cost, other.cost)
