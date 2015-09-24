import copy
import math
from positionplusghost import PositionPlusGhost
from Queue import PriorityQueue

def manhattan_distance(current, dest):
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

#run an astar 1.3-2 with the ghost following a heuristic of the smallest manhattan distance to Pac-Man
#pacman follows the astar algorithm to get the end
#we deal with ghosts by undoing moves in the event that you run into one

#NOTE: THIS ONLY WORKS ON SOME INPUTS FOR MAZE LIKE THE ONE IN newMAZE13.txt
#THE REASON FOR THAT IS BECAUSE SOMETIMES PACMAN GETS STUCK BASED ON HOW WE DID IT IN RELATION TO THE GHOSTS POSITION

def a_star132(maze, start, end, walls):
	#initialize maze2 by copying maze and a priority queue
	maze2 = copy.deepcopy(maze)
	opened = 0
	p_queue = PriorityQueue(maxsize=0)

	#initialize the position of the ghost by checking for the first instance of 'G'
	ghostPos = [0, 0]
	initGhostPos = [0, 0]
	shouldBreak = False
	for i in range(len(walls)):
		for j in range(len(walls[i])):
			if maze2[i][j] is 'G':
				ghostPos = [i, j]
				initGhostPos = [i, j]
				shouldBreak = True
				break
		if(shouldBreak):
			break

	#set ghostDirection to be right at first
	ghostDirection = 'R'
	firstTurn = True

	cost_so_far = {}
	cost = {}
	prev = {}

	b_prev = {}
	b_cost_so_far = {} #If we need to backup and undo a move, we need to keep track of the old state before the mve was made. We will save prev, cost, and cost_so_far for a node
	b_cost = {}

	start_pos = PositionPlusGhost(start, ghostPos, ghostDirection, 0) #Initialize the positon of the pacman, the ghost, the direction and cost
	p_queue.put(start_pos)
	prev[start] = None

	b_prev[start] = None			#If we need to backup and undo a move, we need to keep track of the old state before the mve was made. We will save prev, cost, and cost_so_far for a node
	b_cost_so_far[start] = None
	b_cost[start] = None

	cost_so_far[start] = 0
	cost[start] = 0
	
	while not p_queue.empty():   #While the pqueue is not empty ie there are still moves left for Pacman to do
		current = p_queue.get()  #Pop of the queue
		opened += 1

		x_pos = current.pos[0]
		y_pos = current.pos[1]
		ghostDirection = current.ghost_dir
		ghostPos = current.ghost_pos

		#For visualization sake just have g where the ghost is
		#NOTE: THIS GETS OVERWRITTEN WHEN PACMAN travels back to the beginning in the end
		if(maze2[ghostPos[0]][ghostPos[1]] != 'G' and maze2[ghostPos[0]][ghostPos[1]] != 'P' and maze2[ghostPos[0]][ghostPos[1]] != '.'):
			maze2[ghostPos[0]][ghostPos[1]] = 'g'

		#if pacman's position is equal to ghosts move everything back one step
		if(x_pos == ghostPos[0] and y_pos == ghostPos[1]):
			if current.pos in b_cost:
				cost_so_far[current.pos] = b_cost_so_far[current.pos]
				cost[current.pos] = b_cost[current.pos]
				prev[current.pos] = b_prev[current.pos]
			else:
				del cost_so_far[current.pos]
				del cost[current.pos]
				del prev[current.pos]
			continue

		#prev is not initalized on the firstTurn so you wouldnt check if it wasnt the first turn
		if not firstTurn:
			#check if you've passed through it from any direction
			#if you have follow the same procedure you did for when they were equal and move everything back a step
			if(prev[(x_pos, y_pos)][0] == x_pos and prev[(x_pos, y_pos)][1] == y_pos - 1 and x_pos == ghostPos[0] and y_pos == ghostPos[1] + 1 and ghostDirection is 'L'):
				if current.pos in b_cost:
					cost_so_far[current.pos] = b_cost_so_far[current.pos]
					cost[current.pos] = b_cost[current.pos]
					prev[current.pos] = b_prev[current.pos]
				else:
					del cost_so_far[current.pos]
					del cost[current.pos]
					del prev[current.pos]
				continue

			if(prev[(x_pos, y_pos)][0] == x_pos and prev[(x_pos, y_pos)][1] == y_pos + 1 and x_pos == ghostPos[0] and y_pos == ghostPos[1] - 1 and ghostDirection is 'R'):
				if current.pos in b_cost:
					cost_so_far[current.pos] = b_cost_so_far[current.pos]
					cost[current.pos] = b_cost[current.pos]
					prev[current.pos] = b_prev[current.pos]
				else:
					del cost_so_far[current.pos]
					del cost[current.pos]
					del prev[current.pos]
				continue

			if(prev[(x_pos, y_pos)][0] == x_pos + 1 and prev[(x_pos, y_pos)][1] == y_pos and x_pos == ghostPos[0] - 1 and y_pos == ghostPos[1] and ghostDirection is 'U'):
				if current.pos in b_cost:
					cost_so_far[current.pos] = b_cost_so_far[current.pos]
					cost[current.pos] = b_cost[current.pos]
					prev[current.pos] = b_prev[current.pos]
				else:
					del cost_so_far[current.pos]
					del cost[current.pos]
					del prev[current.pos]
				continue

 			if(prev[(x_pos, y_pos)][0] == x_pos - 1 and prev[(x_pos, y_pos)][1] == y_pos and x_pos == ghostPos[0] + 1 and y_pos == ghostPos[1] and ghostDirection is 'D'):
				if current.pos in b_cost:
					cost_so_far[current.pos] = b_cost_so_far[current.pos]
					cost[current.pos] = b_cost[current.pos]
					prev[current.pos] = b_prev[current.pos]
				else:
					del cost_so_far[current.pos]
					del cost[current.pos]
					del prev[current.pos]
				continue

		#firstTurn will never be trueafter the firstTurn
		firstTurn = False

		#check if pacman's position is the same as the end position: game over
		if x_pos == end[0] and y_pos == end[1]:
			break

		#determine where the ghost moves by taking the manhattan distance from the ghost to the pacman and seeing where the ghost moves
		ghostNeighbors = [(ghostPos[0] -1, ghostPos[1]), (ghostPos[0], ghostPos[1] + 1), (ghostPos[0] + 1, ghostPos[1]), (ghostPos[0], ghostPos[1] - 1)]
		ghostManhattanDistances = []

		index = 0
		for neighbor in ghostNeighbors:
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):
				if not walls[neighbor[0]][neighbor[1]]:
					ghostManhattanDistances.append(manhattan_distance(neighbor, current.pos))

		minimumDistance = min(ghostManhattanDistances)
		for i in range(len(ghostNeighbors)):
			if(manhattan_distance(ghostNeighbors[i], current.pos) == minimumDistance):
				if not walls[ghostNeighbors[i][0]][ghostNeighbors[i][1]]:
					index = i

		#change direction and position based on which direction the ghost moved in
		if(index == 0):
			ghostDirection = 'U'
			ghostPos = [ghostPos[0] - 1, ghostPos[1]]
		elif(index == 1):
			ghostDirection = 'R'
			ghostPos = [ghostPos[0], ghostPos[1] + 1]
		elif(index == 2):
			ghostDirection = 'D'
			ghostPos = [ghostPos[0] + 1, ghostPos[1]]
		else:
			ghostDirection = 'L'
			ghostPos = [ghostPos[0], ghostPos[1] - 1]


		
		#take the manhattan distance from the pacman to the target and see where the pacman should go
		neighbors = [(x_pos -1, y_pos), (x_pos, y_pos + 1), (x_pos + 1, y_pos), (x_pos, y_pos - 1)]

		for neighbor in neighbors:
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):
				if not walls[neighbor[0]][neighbor[1]]:
					if not neighbor in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)):
						new = PositionPlusGhost(neighbor, ghostPos, ghostDirection, cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end))
						if neighbor in cost:	#If we are considering a node again, we need to keep track of the previous values for cost, cost_so_far, and prev so that we can revert it if need be	
							b_cost_so_far[new.pos] = cost_so_far[new.pos]
							b_cost[new.pos] = cost[new.pos]
							b_prev[new.pos] = prev[new.pos]
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + 1
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new) #put it on the pqueue so you can use it later


	#you're done so set the thing to end and backtrack to see how you got to the end increasing steps to the end
	current = end
	steps = 0
	while maze[current[0]][current[1]] != 'P':
		current = prev[(current[0], current[1])]
		if maze[current[0]][current[1]] != 'G':
			maze2[current[0]][current[1]] = '.'
		if maze[current[0]][current[1]] != 'P':
			steps += 1

	maze2[start[0]][start[1]] = 'P'
	maze2[initGhostPos[0]][initGhostPos[1]] = 'G'

	return maze2, cost_so_far[end], opened
	


if __name__ == "__main__":
	maze = [['%', '%', '%', '%', '%'], 
			['%', '%', '%', '%', '%', '%'],
			['%', '', '', '', '%', '%'],
			['%', '', '%', '', '%', '%'],
			['%', '.', '%', '', 'P', '%'],
			['%', '%', '%', '%', '%', '%']]
	walls = [[True, True, True, True, True, True], 
			[True, True, True, True, True, True],
			[True, False, False, False, True, True],
			[True, False, True, False, True, True],
			[True, False, True, False, False,True],
			[True, True, True, True, True, True]]

	path, steps, opened = a_star(maze, (4, 4), (4, 1), walls)
	for line in path:
	 	print(line)

	print(steps)
	print(opened)
