import copy
import math

def greedy(maze, start, end, walls):
	visited = copy.deepcopy(walls)
	prev = copy.deepcopy(maze)
	steps = 0
	nodesExpanded = 0
	currentPoint = start
	minimumPoint = []

	while currentPoint[0] != end[0] or currentPoint[1] != end[1]:
		minManhattanDistance = []
		minManhattanDistancePoints = []
		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):
			break

		if visited[currentPoint[0]][currentPoint[1] - 1] is True and visited[currentPoint[0] + 1][currentPoint[1]] is True and visited[currentPoint[0]][currentPoint[1] + 1] is True and visited[currentPoint[0] - 1][currentPoint[1]] is True:
			steps -= 1
			nodesExpanded += 1
			maze[currentPoint[0]][currentPoint[1]] = ''
			visited[currentPoint[0]][currentPoint[1]] = True
			currentPoint = prev[currentPoint[0]][currentPoint[1]]
		else:
			nodesExpanded += 1

			if not (currentPoint[1] - 1) < 0 and not visited[currentPoint[0]][currentPoint[1] - 1]:
				prev[currentPoint[0]][currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append(math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - 1 - end[1]))
				minManhattanDistancePoints.append([currentPoint[0], currentPoint[1] - 1])

			if not (currentPoint[0] + 1) >= len(walls) and not visited[currentPoint[0] + 1][currentPoint[1]]:
				prev[currentPoint[0] + 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append(math.fabs(currentPoint[0] + 1 - end[0]) + math.fabs(currentPoint[1] - end[1]))
				minManhattanDistancePoints.append([currentPoint[0] + 1, currentPoint[1]])

			if not (currentPoint[1] + 1) >= len(walls) and not visited[currentPoint[0]][currentPoint[1] + 1]:
				prev[currentPoint[0]][currentPoint[1] + 1] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append(math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] + 1 - end[1]))
				minManhattanDistancePoints.append([currentPoint[0], currentPoint[1] + 1])

			if not (currentPoint[0] - 1) < 0 and not visited[currentPoint[0] - 1][currentPoint[1]]:
				prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append(math.fabs(currentPoint[0] - 1 - end[0]) + math.fabs(currentPoint[1] - end[1]))
				minManhattanDistancePoints.append([currentPoint[0] - 1, currentPoint[1]])

			if len(minManhattanDistance) != 0:
				steps += 1
				minimumVal = min(minManhattanDistance)
				# print(minManhattanDistancePoints)
				# print(minimumVal)
				for point in minManhattanDistancePoints:
					print(point)
					print(currentPoint)
					print(math.fabs(point[0] - currentPoint[0]) + math.fabs(point[1] - currentPoint[1]))
					if(math.fabs(point[0] - currentPoint[0]) + math.fabs(point[1] - currentPoint[1]) == minimumVal):
						minimumPoint = [point[0]][point[1]]
						if maze[currentPoint[0]][currentPoint[1]] is not '.':
							maze[currentPoint[0]][currentPoint[1]] = 'g'
							visited[currentPoint[0]][currentPoint[1]] = True
							currentPoint = minimumPoint

			# print(currentPoint)
			# print(end)
			# if maze[currentPoint[0]][currentPoint[1]] is not '.':
			# 	maze[currentPoint[0]][currentPoint[1]] = 'g'
			# visited[currentPoint[0]][currentPoint[1]] = True
			# currentPoint = minimumPoint
			# print(currentPoint)
			# print(end)
	return [steps, nodesExpanded]

if __name__ == "__main__":
	maze = [['%', '%', '%', '%', '%'], 
			['%', '%', '%', '%', '%', '%'],
			['%', '', '', '', '', '%'],
			['%', '', '%', '', '%', '%'],
			['%', '.', '', '', 'P', '%'],
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