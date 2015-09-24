class stack(object):
	"""
	A typical stack with an init, pop and push method
	"""

	def __init__(self):
		"""
		Inits the stack to an empty list
		"""
		self.m_stack = []

	def push(self, value):
		"""
		Inserts value into the stack
		"""
		self.m_stack.append(value)

	def pop(self):
		"""
		Removes the most recently inserted value from the queue and returns it
		"""
		return self.m_stack.pop()

	def isEmpty(self):
		"""
		Returns whether the queue is empty or not
		"""
		return len(self.m_stack) == 0