import copy
import math
import time

def greedy(maze, start, end, walls):
	maze2 = copy.deepcopy(maze)
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)
	steps = 0
	nodesExpanded = 0
	currentPoint = start
	minimumPoint = []

	while currentPoint[0] != end[0] or currentPoint[1] != end[1]:

		minManhattanDistance = []

		nodesExpanded += 1
		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):
			break

		if visited[currentPoint[0]][currentPoint[1] - 1] is True and visited[currentPoint[0] + 1][currentPoint[1]] is True and visited[currentPoint[0]][currentPoint[1] + 1] is True and visited[currentPoint[0] - 1][currentPoint[1]] is True:
			maze2[currentPoint[0]][currentPoint[1]] = ' '
			visited[currentPoint[0]][currentPoint[1]] = True
			currentPoint = prev[currentPoint[0]][currentPoint[1]]
		else:
			if not (currentPoint[1] - 1) < 0 and not visited[currentPoint[0]][currentPoint[1] - 1]:
				prev[currentPoint[0]][currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - 1 - end[1]), [currentPoint[0], currentPoint[1] - 1]])

			if not (currentPoint[0] + 1) >= len(walls) and not visited[currentPoint[0] + 1][currentPoint[1]]:
				prev[currentPoint[0] + 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] + 1 - end[0]) + math.fabs(currentPoint[1] - end[1]), [currentPoint[0] + 1, currentPoint[1]]])

			if not (currentPoint[1] + 1) >= len(walls) and not visited[currentPoint[0]][currentPoint[1] + 1]:
				prev[currentPoint[0]][currentPoint[1] + 1] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] + 1 - end[1]), [currentPoint[0], currentPoint[1] + 1]])

			if not (currentPoint[0] - 1) < 0 and not visited[currentPoint[0] - 1][currentPoint[1]]:
				prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - 1 - end[0]) + math.fabs(currentPoint[1] - end[1]), [currentPoint[0] - 1, currentPoint[1]]])

			if len(minManhattanDistance) != 0:
				minimumVal = minManhattanDistance[0][0]
				for pair in minManhattanDistance:
					if(pair[0] < minimumVal):
						minimumVal = pair[0]

				for pair in minManhattanDistance:
					if(pair[0] == minimumVal):
						if maze[pair[1][0]][pair[1][1]] is not '.' or maze[pair[1][0]][pair[1][1]]  is not 'P':
							visited[currentPoint[0]][currentPoint[1]] = True
							currentPoint = [pair[1][0], pair[1][1]]

	maze2[start[0]][start[1]] = 'P'
	maze2[end[0]][end[1]] = '.'
	return [maze2, steps, nodesExpanded]

if __name__ == "__main__":
	maze = [['%', '%', '%', '%', '%'], 
			['%', '%', '%', '%', '%', '%'],
			['%', '', '', '', '', '%'],
			['%', '', '%', '', '%', '%'],
			['%', 'P', '%', '', '.', '%'],
			['%', '%', '%', '%', '%', '%']]
	walls = [[True, True, True, True, True, True], 
			[True, True, True, True, True, True],
			[True, False, False, False, True, True],
			[True, False, True, False, True, True],
			[True, False, True, False, False,True],
			[True, True, True, True, True, True]]

	resp = greedy(maze, [4, 1], [4, 4], walls)
	print(resp)