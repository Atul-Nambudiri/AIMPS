def bfs(maze, start, end, walls):
	m_queue = queue()
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(walls)
	steps = 0

	m_queue.enqueue(currentPoint)

	while not m_queue.isEmpty():
		currentPoint = m_queue.dequeue()
		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):
			break

		#implicit else
		if not visited[currentPoint[0], currentPoint[1] - 1]:
			prev[currentPoint[0], currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
			m_queue.enqueue([currentPoint[0], currentPoint[1] - 1])

		if not visited[currentPoint[0] + 1, currentPoint[1]]:
			prev[currentPoint[0], currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
			m_queue.enqueue([currentPoint[0] + 1, currentPoint[1]])

		if not visited[currentPoint[0], currentPoint[1] + 1]:
			prev[currentPoint[0], currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
			m_queue.enqueue([currentPoint[0], currentPoint[1] + 1])

		if not visited[currentPoint[0] - 1, currentPoint[1]]:
			prev[currentPoint[0], currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
			m_queue.enqueue([currentPoint[0] - 1, currentPoint[1]])

