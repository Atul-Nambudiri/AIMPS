class queue(object):
	"""
	A typical queue with an init, enqueue and dequeue method
	"""

	def __init__(self):
		"""
		Inits the queue to an empty list
		"""
		self.m_queue = []

	def enqueue(self, value):
		"""
		Inserts value into the queue
		"""
		self.m_queue.append(value)

	def dequeue(self):
		"""
		Removes the first inserted value from the queue and returns it
		"""
		return self.m_queue.pop(0)

	def isEmpty(self):
		"""
		Returns whether the queue is empty or not
		"""
		return self.m_queue == 0;