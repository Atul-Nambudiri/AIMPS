import copy
import math
from position import Position
from Queue import PriorityQueue

def manhattan_distance(current, dest):
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

def a_star13(maze, start, end, walls):
	maze2 = copy.deepcopy(maze)
	opened = 0
	p_queue = PriorityQueue(maxsize=0)

	cost_so_far = {}
	cost = {}
	prev = {}

	start_pos = Position(start, 0)
	p_queue.put(start_pos)
	prev[start] = None
	cost_so_far[start] = 0
	cost[start] = 0


	#initialize the position of the ghost by checking for the first instance where there is no wall
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

	while not p_queue.empty():
		current = p_queue.get()

		x_pos = current.pos[0]
		y_pos = current.pos[1]

		#if pacman's position is equal to ghosts
		if(x_pos == ghostPos[0] and y_pos == ghostPos[1]):
			print("GAME OVER1")
			end = current.pos
			break

		if not firstTurn:
			#check if you pass through it
			if(prev[(x_pos, y_pos)][0] == x_pos and prev[(x_pos, y_pos)][1] == y_pos - 1 and x_pos == ghostPos[0] and y_pos == ghostPos[1] + 1 and ghostDirection is 'L'):
				print("GAME OVER2")
				end = current.pos
				break

			if(prev[(x_pos, y_pos)][0] == x_pos and prev[(x_pos, y_pos)][1] == y_pos + 1 and x_pos == ghostPos[0] and y_pos == ghostPos[1] - 1 and ghostDirection is 'R'):
				print("GAME OVER3")
				end = current.pos
				break

		firstTurn = False

		#check if pacman's position is the same as the end position: game over
		if x_pos == end[0] and y_pos == end[1]:
			print("YOU WIN")
			break

		#updating the ghosts position
		#if the ghost's direction is R and there is no wall, move it to the right
		#if there is a wall, change the direction so that it's going the other way
		#likewise the same logic applies for the ghost's direction being L
		if(ghostDirection is 'R'):
			if(walls[ghostPos[0]][ghostPos[1] + 1]):
				ghostDirection = 'L'
				ghostPos = [ghostPos[0], ghostPos[1] - 1]
			else:
				ghostPos = [ghostPos[0], ghostPos[1] + 1]
		else:
			if(walls[ghostPos[0]][ghostPos[1] - 1]):
				ghostDirection = 'R'
				ghostPos = [ghostPos[0], ghostPos[1] + 1]
			else:
				ghostPos = [ghostPos[0], ghostPos[1] - 1]

		#check if pacman's will pass through the ghost on it's next iteration
		# if(x_pos == ghostPos[0] and y_pos == ghostPos[1]):
		# 	print("GAME OVER")
		# 	break

		# if(maze2[ghostPos[0]][ghostPos[1]] != 'G' and maze2[ghostPos[0]][ghostPos[1]] != 'P'):
		# 	maze2[ghostPos[0]][ghostPos[1]] = 'g'

		opened += 1

		neighbors = [(x_pos -1, y_pos), (x_pos, y_pos + 1), (x_pos + 1, y_pos), (x_pos, y_pos - 1)]

		for neighbor in neighbors:
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):
				if not walls[neighbor[0]][neighbor[1]]:
					if neighbor not in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)):
						new = Position(neighbor, cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end))
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + 1
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new)

	current = end
	steps = 0

	while maze[current[0]][current[1]] != 'P':
		current = prev[(current[0], current[1])]
		if maze[current[0]][current[1]] != 'G' and maze[current[0]][current[1]] != 'g':
			maze2[current[0]][current[1]] = '.'
		steps += 1

	maze2[start[0]][start[1]] = 'P'
	maze2[initGhostPos[0]][initGhostPos[1]] = 'G'

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
