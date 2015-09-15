class queue(object):
	# a typical queue with an init, enqueue and dequeue method

	def __init__(self):
		self.m_queue = []

	def enqueue(self, value):
		self.m_queue.append(value)

	def dequeue(self):
		return self.m_queue.popleft()

	def isEmpty(self):
		return self.m_queue == 0;