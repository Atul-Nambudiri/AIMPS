import copy
import math

def greedy(maze, start, end, walls):
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(walls)
	steps = 0
	nodesExpanded = 0
	currentPoint = start

	while currentPoint[0] != end[0] and currentPoint[1] != end[1]:
		nextPoint = currentPoint
		manhattanDistance = math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - end[1])
		nodesExpanded += 1
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
				manhattanDistance = min(manhattanDistance, math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - 1 - end[1]))
				if manhattanDistance > math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - 1 - end[1]):
					nextPoint = [currentPoint[0], currentPoint[1] - 1]

			if not (currentPoint[0] + 1) >= len(walls) and not visited[currentPoint[0] + 1][currentPoint[1]]:
				prev[currentPoint[0] + 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				manhattanDistance = min(manhattanDistance, math.fabs(currentPoint[0] + 1 - end[0]) + math.fabs(currentPoint[1] - end[1]))
				if manhattanDistance > math.fabs(currentPoint[0] + 1 - end[0]) + math.fabs(currentPoint[1] - end[1]):
					nextPoint = [currentPoint[0] + 1, currentPoint[1]]

			if not (currentPoint[1] + 1) >= len(walls) and not visited[currentPoint[0]][currentPoint[1] - 1]:
				prev[currentPoint[0]][currentPoint[1] + 1] = [currentPoint[0], currentPoint[1]]
				manhattanDistance = min(manhattanDistance, math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] + 1 - end[1]))
				if manhattanDistance > math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] + 1 - end[1]):
					nextPoint = [currentPoint[0], currentPoint[1] + 1]

			if not (currentPoint[0] - 1) < 0 and not visited[currentPoint[0]][currentPoint[1] - 1]:
				prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				manhattanDistance = min(manhattanDistance, math.fabs(currentPoint[0] - 1 - end[0]) + math.fabs(currentPoint[1] - end[1]))
				if manhattanDistance > math.fabs(currentPoint[0] - 1 - end[0]) + math.fabs(currentPoint[1] - end[1]):
					nextPoint = [currentPoint[0] - 1, currentPoint[1]]

		steps += 1

		currentPoint = nextPoint

		if maze[currentPoint[0]][currentPoint[1]] is not '.':
			maze[currentPoint[0]][currentPoint[1]] = 'g'
		visited[currentPoint[0]][currentPoint[1]] = True

	return [steps, nodesExpanded]

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
			[True, False, False, False, False,True],
			[True, True, True, True, True, True]]

	resp = greedy(maze, [4, 1], [4, 4], walls)
	print(resp)
	print(maze)