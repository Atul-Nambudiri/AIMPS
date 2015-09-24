from stack import stack
import copy

def dfs(maze, start, end, walls):
	"""
	This function runs DFS on the maze to find a path from start to end
	"""
	m_stack = stack()			#Inits a stack to store nodes in
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)		#Keeps track of the previous for a particular node
	opened = 0
	m_stack.push(start)				#Put in start into the stack
	prev[start[0]][start[1]] = None			
	
	#Iterate until the stack is empty 
	while not m_stack.isEmpty():
		opened += 1
		current = m_stack.pop()				#Remove a node from the stack

		if visited[current[0]][current[1]] == False:	
			visited[current[0]][current[1]] = True
			if current[0] == end[0] and current[1] == end[1]:	#If you have reached the end, return
				break
			else: #This checks all neighbors, top, right, bottom, left, to see if we can move there
				if not (current[0] - 1) < 0 and not visited[current[0] -1][current[1]]:
					prev[current[0] -1][current[1]] = [current[0], current[1]]				#Set the previous for the neighbor to be the current node
					m_stack.push([current[0] -1 , current[1]])								#Push it onto the stack
	
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
	while maze[current[0]][current[1]] != 'P':				#Go to the end point, and build out the solution path back to the start by following the previous values for each node
		current = prev[current[0]][current[1]]
		path[current[0]][current[1]] = '.'
		steps += 1											#Keep track of the number of steps you have taken
	path[start[0]][start[1]] = 'P'

	return path, steps, opened								#Return the path, solution cost, and number of nodes expanded



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

	print("Steps: %s" % (steps))
	print("Nodes Visited: %s" % (opened))
