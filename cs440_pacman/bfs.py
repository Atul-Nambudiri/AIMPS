from queue import queue
import copy

def bfs(maze, start, end, walls):
	m_queue = queue()
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(walls)
	steps = 0

	m_queue.enqueue(start)

	while not m_queue.isEmpty():
		currentPoint = m_queue.dequeue()
		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):
			break

		if visited[currentPoint[0]][currentPoint[1] - 1] is True and visited[currentPoint[0] + 1][currentPoint[1]] is True and visited[currentPoint[0]][currentPoint[1] + 1] is True and visited[currentPoint[0] - 1][currentPoint[1]] is True:
			steps -= 1
			maze[currentPoint[0]][currentPoint[1]] = ''
			visited[currentPoint[0]][currentPoint[1]] = True
			currentPoint = prev[currentPoint[0]][currentPoint[1]]

		else:
			if not (currentPoint[1] - 1) < 0 and not visited[currentPoint[0]][currentPoint[1] - 1]:
				prev[currentPoint[0]][currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
				m_queue.enqueue([currentPoint[0], currentPoint[1] - 1])

			if not (currentPoint[0] + 1) >= len(walls) and not visited[currentPoint[0] + 1][currentPoint[1]]:
				prev[currentPoint[0] + 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				m_queue.enqueue([currentPoint[0] + 1, currentPoint[1]])

			if not (currentPoint[1] + 1) >= len(walls[0]) and not visited[currentPoint[0]][currentPoint[1] + 1]:
				prev[currentPoint[0]][currentPoint[1] + 1] = [currentPoint[0], currentPoint[1]]
				m_queue.enqueue([currentPoint[0], currentPoint[1] + 1])

			if not (currentPoint[0] - 1) < 0 and not visited[currentPoint[0] - 1][currentPoint[1]]:
				print(currentPoint)
				prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				m_queue.enqueue([currentPoint[0] - 1, currentPoint[1]])

			steps += 1
			if maze[currentPoint[0]][currentPoint[1]] is not 'P':
				maze[currentPoint[0]][currentPoint[1]] = 'g'
			visited[currentPoint[0]][currentPoint[1]] = True

	return steps

if __name__ == "__main__":
	maze = [['%', '%', '%', '%', '%'], 
			['%', '%', '%', '%', '%', '%'],
			['%', '', '', '', '', '%'],
			['%', '', '%', '', '%', '%'],
			['%', '.', '%', '', 'P', '%'],
			['%', '%', '%', '%', '%', '%']]
	walls = [[True, True, True, True, True, True], 
			[True, True, True, True, True, True],
			[True, False, False, False, True, True],
			[True, False, True, False, True, True],
			[True, False, True, False, False,True],
			[True, True, True, True, True, True]]

	resp = bfs(maze, [4, 1], [4, 4], walls)
	print(resp)
	print(maze)