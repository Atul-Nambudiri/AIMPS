from queue import queue
import copy


# this function runs a breadth first search algorithm in order to find a path from start to the end
def bfs(maze, start, end, walls):

	#initialize everything you have to, a copy of the maze, a queue, visited and previous so you can go back
	maze2 = copy.deepcopy(maze)
	m_queue = queue()
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)
	steps = 0
	nodesExpanded = 0

	m_queue.enqueue(start)  #push start onto the queue

	#iterate until the queue is empty
	while not m_queue.isEmpty():
		currentPoint = m_queue.dequeue() #remove a node from the stack and expand it
		nodesExpanded += 1

		if visited[currentPoint[0]][currentPoint[1]] is False: #if you havent visited the node yet
			visited[currentPoint[0]][currentPoint[1]] = True
			if(currentPoint[0] == end[0] and currentPoint[1] == end[1]): #break if you've reached the end
				break

			else:
				if not (currentPoint[1] - 1) < 0 and not visited[currentPoint[0]][currentPoint[1] - 1]:
					prev[currentPoint[0]][currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]  #set the previous for the next node to be the current node
					m_queue.enqueue([currentPoint[0], currentPoint[1] - 1])                          #and add it onto the queue

				if not (currentPoint[0] + 1) >= len(walls) and not visited[currentPoint[0] + 1][currentPoint[1]]:
					prev[currentPoint[0] + 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
					m_queue.enqueue([currentPoint[0] + 1, currentPoint[1]])

				if not (currentPoint[1] + 1) >= len(walls[0]) and not visited[currentPoint[0]][currentPoint[1] + 1]:
					prev[currentPoint[0]][currentPoint[1] + 1] = [currentPoint[0], currentPoint[1]]
					m_queue.enqueue([currentPoint[0], currentPoint[1] + 1])

				if not (currentPoint[0] - 1) < 0 and not visited[currentPoint[0] - 1][currentPoint[1]]:
					prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
					m_queue.enqueue([currentPoint[0] - 1, currentPoint[1]])

	current = end
	steps = 0
	while maze[current[0]][current[1]] != 'P':  #make out a solution path from the endpoint going backwards incrementing to steps everytime
		current = prev[current[0]][current[1]]
		maze2[current[0]][current[1]] = '.'
		steps += 1
	maze2[start[0]][start[1]] = 'P'

	return maze2, steps, nodesExpanded

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

	"""resp = bfs(maze, [4, 1], [4, 4], walls)
	for line in resp[0]:
		print(line)"""

	maze2, steps, nodesExpanded = bfs(maze, (4, 4), (4, 1), walls)
	for line in maze2:
		print(line)

	print("Steps: %s" % (steps))
	print("Nodes Visited: %s" % (nodesExpanded))

