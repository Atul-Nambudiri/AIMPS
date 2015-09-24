import copy
import math
from position import Position
from Queue import PriorityQueue

def manhattan_distance(current, dest):
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

def a_star132(maze, start, end, walls):
	maze2 = copy.deepcopy(maze)
	opened = 0
	p_queue = PriorityQueue(maxsize=0)
	ghostP_queue = PriorityQueue(maxsize=0)

	cost_so_far = {}
	cost = {}
	prev = {}
	ghost_prev = {}

	start_pos = Position(start, 0)
	p_queue.put(start_pos)
	prev[start] = None
	cost_so_far[start] = 0
	cost[start] = 0

	ghost_cost = {}
	ghost_cost_so_far = {}


	#initialize the position of the ghost by checking for the first instance where there is no wall
	ghostPos = [0, 0]
	initGhostPos = [0, 0]
	shouldBreak = False
	for i in range(len(walls)):
		for j in range(len(walls[i])):
			if maze2[i][j] is 'G':
				ghostPos = Position((i, j), 0)
				initGhostPos = Position((i, j), 0)
				ghost_cost[(i, j)] = 0
				ghost_cost_so_far[(i, j)] = 0
				shouldBreak = True
				break
		if(shouldBreak):
			break
	ghostP_queue.put(ghostPos)
	

	#set ghostDirection to be right at first
	ghostDirection = 'R'
	firstTurn = True

	while not p_queue.empty():
		current = p_queue.get()
		ghostPos = ghostP_queue.get()

		x_pos = current.pos[0]
		y_pos = current.pos[1]

		ghostx_pos = ghostPos.pos[0]
		ghosty_pos = ghostPos.pos[1]
		print(str(ghostx_pos) +" , " +str(ghosty_pos))

		ghostEnd = end
		#if pacman's position is equal to ghosts
		if(x_pos == ghostx_pos and y_pos == ghosty_pos):
			print("GAME OVER1")
			end = prev[(current.pos[0], current.pos[1])]
			ghostEnd = end
			break

		
		if not firstTurn:
			#check if you've passed through it
			directionChecker = ghost_prev[(ghostx_pos, ghosty_pos)]
			if(directionChecker[0] == ghostx_pos + 1):
				ghostDirection = 'U'
			elif(directionChecker[0] == ghostx_pos - 1):
				ghostDirection = 'D'
			elif(directionChecker[1] == ghosty_pos + 1):
				ghostDirection = 'L'
			else:
				ghostDirection = 'R'

			if(prev[(x_pos, y_pos)][0] == x_pos and prev[(x_pos, y_pos)][1] == y_pos - 1 and x_pos == ghostx_pos and y_pos == ghosty_pos + 1 and ghostDirection is 'L'):
				print("GAME OVER2")
				end = prev[(current.pos[0], current.pos[1])]
				ghostEnd = (end[0], end[1] - 1)
				break

			if(prev[(x_pos, y_pos)][0] == x_pos and prev[(x_pos, y_pos)][1] == y_pos + 1 and x_pos == ghostx_pos and y_pos == ghosty_pos - 1 and ghostDirection is 'R'):
				print("GAME OVER3")
				end = prev[(current.pos[0], current.pos[1])]
				ghostEnd = (end[0], end[1] + 1)
				break
			if(prev[(x_pos, y_pos)][0] == x_pos + 1 and prev[(x_pos, y_pos)][1] == y_pos and x_pos == ghostx_pos - 1 and y_pos == ghosty_pos and ghostDirection is 'U'):
				print("GAME OVER4")
				end = prev[(current.pos[0], current.pos[1])]
				ghostEnd = (end[0] + 1, end[1])
				break

			if(prev[(x_pos, y_pos)][0] == x_pos - 1 and prev[(x_pos, y_pos)][1] == y_pos and x_pos == ghostx_pos + 1 and y_pos == ghosty_pos and ghostDirection is 'D'):
				print("GAME OVER5")
				end = prev[(current.pos[0], current.pos[1])]
				ghostEnd = (end[0] - 1, end[1])
				break

		if maze[ghostx_pos][ghosty_pos] != 'P' and maze[ghostx_pos][ghosty_pos] != '.':
			maze2[ghostx_pos][ghosty_pos] = 'g'

		firstTurn = False

		#check if pacman's position is the same as the end position: game over
		if x_pos == end[0] and y_pos == end[1]:
			print("YOU WIN")
			ghostEnd = ghostPos.pos
			break

		#updating the ghosts position
		ghostNeighbors = [(ghostx_pos -1, ghosty_pos), (ghostx_pos, ghosty_pos + 1), (ghostx_pos + 1, ghosty_pos), (ghostx_pos, ghosty_pos - 1)]

		for neighbor in ghostNeighbors:
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):
				if not walls[neighbor[0]][neighbor[1]]:
					if not neighbor in ghost_cost or ghost_cost[neighbor] > (ghost_cost_so_far[(ghostx_pos, ghosty_pos)] + 1 + manhattan_distance(ghostPos.pos, current.pos)):
						new = Position(neighbor, ghost_cost_so_far[(ghostx_pos, ghosty_pos)] + 1 + manhattan_distance(current.pos, ghostPos.pos))
						ghost_cost_so_far[new.pos] = ghost_cost_so_far[(ghostx_pos, ghosty_pos)] + 1
						ghost_cost[new.pos] = ghost_cost_so_far[(ghostx_pos, ghosty_pos)] + 1 + manhattan_distance(current.pos, ghostPos.pos)
						if(new.pos not in ghost_prev):
							ghost_prev[new.pos] = [ghostx_pos, ghosty_pos]
						ghostP_queue.put(new)

		opened += 1
		
		neighbors = [(x_pos -1, y_pos), (x_pos, y_pos + 1), (x_pos + 1, y_pos), (x_pos, y_pos - 1)]

		for neighbor in neighbors:
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):
				if not walls[neighbor[0]][neighbor[1]]:
					if not neighbor in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)):
						new = Position(neighbor, cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end))
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + 1
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new)

	current = end
	steps = 0
	ghostPos = ghostEnd

	while maze[ghostPos[0]][ghostPos[1]] != 'G':
		ghostPos = ghost_prev[(ghostPos[0], ghostPos[1])]
		if maze[ghostPos[0]][ghostPos[1]] != 'P' and maze[ghostPos[0]][ghostPos[1]] != '.':
			maze2[ghostPos[0]][ghostPos[1]] = 'g'

	while maze[current[0]][current[1]] != 'P':
		current = prev[(current[0], current[1])]
		if maze[current[0]][current[1]] != 'G':
			maze2[current[0]][current[1]] = '.'
		if maze[current[0]][current[1]] != 'P':
			steps += 1

	maze2[start[0]][start[1]] = 'P'
	maze2[initGhostPos.pos[0]][initGhostPos.pos[1]] = 'G'

	return maze2, steps, opened
	


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
