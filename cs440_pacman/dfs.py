from stack import stack
import copy

def dfs(maze, start, end, walls):
	m_stack = stack()
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)

	print(start)
	m_stack.push(start)
	prev[start[0]][start[1]] = None
	
	while not m_stack.isEmpty():
		current = m_stack.pop()

		visited[current[0]][current[1]] = True
		if current[0] == end[0] and current[1] == end[1]:
			return prev
		else: #This checks all neighbors, top, right, bottom, left, to see if we can move there
			if not (current[0] - 1) < 0 and not visited[current[0] -1][current[1]]:
				print(1)
				prev[current[0] -1][current[1]] = [current[0], current[1]]
				m_stack.push([current[0] -1 , current[1]])

			if not (current[0] + 1) >= len(walls) and not visited[current[0] + 1][current[1]]:
				print(2)
				prev[current[0] + 1][current[1]] = [current[0], current[1]]
				m_stack.push([current[0] + 1 , current[1]])

			if not (current[1] + 1) >= len(walls[0]) and not visited[current[0]][current[1] + 1]:
				print(3)
				prev[current[0]][current[1] + 1] = [current[0], current[1]]
				m_stack.push([current[0], current[1] + 1]) 

			if not (current[1] - 1) < 0 and not visited[current[0]][current[1] - 1]:
				print(4)
				prev[current[0]][current[1] - 1] = [current[0], current[1]]
				m_stack.push([current[0] , current[1] - 1])

	return prev



if __name__ == "__main__":
	maze = [['%', '%', '%', '%', '%'], 
			['%', '%', '%', '%', '%', '%'],
			['%', '', '', '', '', '%'],
			['%', '', '%', '', '%', '%'],
			['%', '', '%', '', '', 'P'],
			['%', '.', '%', '%', '%', '%']]
	walls = [[True, True, True, True, True, True], 
			[True, True, True, True, True, True],
			[True, False, False, False, True, True],
			[True, False, True, False, True, True],
			[True, False, True, False, False,False],
			[True, True, True, True, True, True]]

	resp = dfs(maze, [5, 1], [4, 5], walls)
	for row in resp:
		print(row)
