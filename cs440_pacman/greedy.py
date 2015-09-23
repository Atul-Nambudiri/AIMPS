import copy
import math
import time

def greedy(maze, start, end, walls):
	maze2 = copy.deepcopy(maze)
	prev = copy.deepcopy(maze)
	visited = copy.deepcopy(walls)
	steps = 0
	nodesExpanded = 0
	currentPoint = start
	minimumPoint = []
	haveBeen = {}

	timeout = time.time() + 15

	while True:
		minManhattanDistance = []

		if(time.time() > timeout):
			end = currentPoint
			print("There was a loop")
			break

		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):
			break

		else:
			visited[currentPoint[0]][currentPoint[1]] = True

			if not (currentPoint[1] - 1) < 0 and not walls[currentPoint[0]][currentPoint[1] - 1]:
				if not visited[currentPoint[0]][currentPoint[1] - 1]:
					prev[currentPoint[0]][currentPoint[1] - 1] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - 1 - end[1]), [currentPoint[0], currentPoint[1] - 1]])

			if not (currentPoint[0] + 1) >= len(walls) and not walls[currentPoint[0] + 1][currentPoint[1]]:
				if not visited[currentPoint[0] + 1][currentPoint[1]]:
					prev[currentPoint[0] + 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] + 1 - end[0]) + math.fabs(currentPoint[1] - end[1]), [currentPoint[0] + 1, currentPoint[1]]])

			if not (currentPoint[1] + 1) >= len(walls) and not walls[currentPoint[0]][currentPoint[1] + 1]:
				if not visited[currentPoint[0]][currentPoint[1] + 1]:
					prev[currentPoint[0]][currentPoint[1] + 1] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] + 1 - end[1]), [currentPoint[0], currentPoint[1] + 1]])

			if not (currentPoint[0] - 1) < 0 and not walls[currentPoint[0] - 1][currentPoint[1]]:
				if not visited[currentPoint[0] - 1][currentPoint[1]]:
					prev[currentPoint[0] - 1][currentPoint[1]] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - 1 - end[0]) + math.fabs(currentPoint[1] - end[1]), [currentPoint[0] - 1, currentPoint[1]]])

			
			if len(minManhattanDistance) != 0:
				minimumVal = minManhattanDistance[0][0]
				for pair in minManhattanDistance:
					if(pair[0] < minimumVal):
						minimumVal = pair[0]

				for pair in minManhattanDistance:
					if(pair[0] == minimumVal):
						if prev[currentPoint[0]][currentPoint[1]] == [pair[1][0], pair[1][1]]:
						 	timeout = time.time()
						else:
						 	currentPoint = (pair[1][0], pair[1][1])
						 	if(currentPoint not in haveBeen):
						 		haveBeen[currentPoint] = 0
						 		nodesExpanded += 1
						 		break

	current = end
	steps = 0

	while maze[current[0]][current[1]] != 'P':
		current = prev[current[0]][current[1]]
		maze2[current[0]][current[1]] = '.'
		if maze[current[0]][current[1]] != 'P':
			steps += 1
	maze2[start[0]][start[1]] = 'P'
	maze2[end[0]][end[1]] = '.'


	return maze2, steps, nodesExpanded

if __name__ == "__main__":
	maze = [['%', '%', '%', '%', '%'], 
			['%', '%', '%', '%', '%', '%'],
			['%', '', '', '', '', '%'],
			['%', '', '%', '', '%', '%'],
			['%', 'P', '', '', '.', '%'],
			['%', '%', '%', '%', '%', '%']]
	walls = [[True, True, True, True, True, True], 
			[True, True, True, True, True, True],
			[True, False, False, False, True, True],
			[True, False, True, False, True, True],
			[True, False, False, False, False,True],
			[True, True, True, True, True, True]]

	resp = greedy(maze, [4, 1], [4, 4], walls)
	print(resp)