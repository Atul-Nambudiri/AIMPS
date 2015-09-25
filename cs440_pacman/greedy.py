import copy
import math
import time

#uses the manhattan distance heuristic and the greedy algorithm to find the best way to get from start to finish
def greedy(maze, start, end, walls):

	#initializes a deep copy of the maze, previous and visited

	maze2 = copy.deepcopy(maze)
	prev = {}
	visited = copy.deepcopy(walls)
	steps = 0
	nodesExpanded = 0
	currentPoint = start

	while True: #assumes that you will be able to find a solution
		minManhattanDistance = []

		if(currentPoint[0] == end[0] and currentPoint[1] == end[1]):  #if you've reached the end then youre done
			break

		#if you've reached a point where all 4 nodes around you are visited then you need to backtrack
		if(visited[currentPoint[0]][currentPoint[1] - 1] and visited[currentPoint[0] + 1][currentPoint[1]] and visited[currentPoint[0]][currentPoint[1] + 1] and visited[currentPoint[0] - 1][currentPoint[1]]):
			visited[currentPoint[0]][currentPoint[1]] = True
			currentPoint = prev[(currentPoint[0], currentPoint[1])]

		else:
			visited[currentPoint[0]][currentPoint[1]] = True

			#if you havent visited the node then you need to set previous of the new node to be the node and append it to manhattan distances provided it meets not visited and in bounds
			if not (currentPoint[1] - 1) < 0 and not visited[currentPoint[0]][currentPoint[1] - 1]:
				prev[(currentPoint[0], currentPoint[1] - 1)] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] - 1 - end[1]), [currentPoint[0], currentPoint[1] - 1]])

			if not (currentPoint[0] + 1) >= len(walls) and not visited[currentPoint[0] + 1][currentPoint[1]]:
				prev[(currentPoint[0] + 1, currentPoint[1])] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] + 1 - end[0]) + math.fabs(currentPoint[1] - end[1]), [currentPoint[0] + 1, currentPoint[1]]])

			if not (currentPoint[1] + 1) >= len(walls[0]) and not visited[currentPoint[0]][currentPoint[1] + 1]:
				prev[(currentPoint[0], currentPoint[1] + 1)] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - end[0]) + math.fabs(currentPoint[1] + 1 - end[1]), [currentPoint[0], currentPoint[1] + 1]])

			if not (currentPoint[0] - 1) < 0 and not visited[currentPoint[0] - 1][currentPoint[1]]:
				prev[(currentPoint[0] - 1, currentPoint[1])] = [currentPoint[0], currentPoint[1]]
				minManhattanDistance.append([math.fabs(currentPoint[0] - 1 - end[0]) + math.fabs(currentPoint[1] - end[1]), [currentPoint[0] - 1, currentPoint[1]]])

			#if the length is not 0 then you need to check it for a min val and then check to see which point equals it
			#set currentPoint afterwards and add 1 to nodes expanded because you've visited a new node
			if len(minManhattanDistance) != 0:
				minimumVal = minManhattanDistance[0][0]
				for pair in minManhattanDistance:
					if(pair[0] < minimumVal):
						minimumVal = pair[0]

				for pair in minManhattanDistance:
					if(pair[0] == minimumVal):
						currentPoint = (pair[1][0], pair[1][1])
						nodesExpanded += 1
						break

	current = end
	steps = 0

	#backtrack and see how many steps it took to get to the end
	while maze[current[0]][current[1]] != 'P':
		current = prev[(current[0], current[1])]
		maze2[current[0]][current[1]] = '.'
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