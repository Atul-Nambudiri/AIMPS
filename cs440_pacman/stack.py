class stack(object):
	# a typical stack with an init, pop and push method

	def __init__(self):
		self.m_stack = []

	def push(self, value):
		self.m_stack.append(value)

	def pop(self):
		return self.m_stack.pop()

	def isEmpty(self):
		return len(self.m_stack) == 0