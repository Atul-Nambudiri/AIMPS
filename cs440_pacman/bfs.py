from queue import queue
import copy

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

		if visited[currentPoint[0], currentPoint[1] - 1] is true and visited[currentPoint[0] + 1, currentPoint[1]] is true and visited[currentPoint[0], currentPoint[1] + 1] is true and visited[currentPoint[0] - 1, currentPoint[1]] is true:
			steps -= 1
			visited[currentPoint[0], currentPoint[1]] = true
			currentPoint = prev

		#implicit else
		else:
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

			steps += 1
			visited[currentPoint[0], currentPoint[1]] = true