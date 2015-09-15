class stack(object):
	# a typical stack with an init, pop and push method

	list m_stack

	def init(self):
		m_stack = []

	def push(self, value):
		m_stack.append(value)

	def pop(self):
		m_stack.pop()