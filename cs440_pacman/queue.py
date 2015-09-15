class queue(object):
	# a typical queue with an init, enqueue and dequeue method

	list m_queue

	def init(self):
		m_queue = []

	def enqueue(self, value):
		m_queue.append(value)

	def dequeue(self):
		m_queue.popleft()

	def isEmpty(self):
		return m_queue == 0;