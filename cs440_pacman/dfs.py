from stack import stack
import copy

def dfs(maze, start, end, walls):
	m_stack = stack()
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)
	opened = 0
	m_stack.push(start)
	prev[start[0]][start[1]] = None
	
	while not m_stack.isEmpty():
		opened += 1
		current = m_stack.pop()

		visited[current[0]][current[1]] = True
		if current[0] == end[0] and current[1] == end[1]:
			break
		else: #This checks all neighbors, top, right, bottom, left, to see if we can move there
			if not (current[0] - 1) < 0 and not visited[current[0] -1][current[1]]:
				prev[current[0] -1][current[1]] = [current[0], current[1]]
				m_stack.push([current[0] -1 , current[1]])

			if not (current[1] + 1) >= len(walls[0]) and not visited[current[0]][current[1] + 1]:
				prev[current[0]][current[1] + 1] = [current[0], current[1]]
				m_stack.push([current[0], current[1] + 1]) 

			if not (current[0] + 1) >= len(walls) and not visited[current[0] + 1][current[1]]:
				prev[current[0] + 1][current[1]] = [current[0], current[1]]
				m_stack.push([current[0] + 1 , current[1]])

			if not (current[1] - 1) < 0 and not visited[current[0]][current[1] - 1]:
				prev[current[0]][current[1] - 1] = [current[0], current[1]]
				m_stack.push([current[0] , current[1] - 1])

	path = copy.deepcopy(maze)
	current = end
	steps = 0
	while maze[current[0]][current[1]] != '.':
		current = prev[current[0]][current[1]]
		path[current[0]][current[1]] = '.'
		steps += 1

	return path, steps, opened



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

	path, steps, opened = dfs(maze, (4, 1), (4, 4), walls)
	for line in path:
		print(line)

	print(steps)
	print(opened)