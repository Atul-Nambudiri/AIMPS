from queue import queue
import copy

def bfs(maze, start, end, walls):
	maze2 = copy.deepcopy(maze)
	m_queue = queue()
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)
	steps = 0
	nodesExpanded = 0

	m_queue.enqueue(start)

	while not m_queue.isEmpty():
		currentPoint = m_queue.dequeue()
		nodesExpanded += 1
		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):
			break

		if visited[currentPoint[0]][currentPoint[1] - 1] is True and visited[currentPoint[0] + 1][currentPoint[1]] is True and visited[currentPoint[0]][currentPoint[1] + 1] is True and visited[currentPoint[0] - 1][currentPoint[1]] is True:
			steps -= 1
			maze2[currentPoint[0]][currentPoint[1]] = ''
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
				prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				m_queue.enqueue([currentPoint[0] - 1, currentPoint[1]])

			steps += 1

			if maze[currentPoint[0]][currentPoint[1]] is not '.':
				maze2[currentPoint[0]][currentPoint[1]] = '.'
			visited[currentPoint[0]][currentPoint[1]] = True

	return [maze2, steps, nodesExpanded]

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
	for line in resp[0]:
		print(line)

	print("Steps: %s" % (resp[1]))
	print("Nodes Visited: %s" % (resp[2]))

