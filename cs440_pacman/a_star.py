import copy
import math
from position import Position
from Queue import PriorityQueue

def manhattan_distance(current, dest):
	"""
	This function calculates the manhattan distance between two points current and dest
	"""
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

def a_star(maze, start, end, walls):
	"""
	Find the best path from start to end using the a_star algorithm
	"""
	opened = 0
	p_queue = PriorityQueue(maxsize=0)			#Use a priority queue to get the position with the highest priority

	cost_so_far = {}					#This dictionary keep track of the number of steps taken to reach a particular point
	cost = {}						#This dictionary keeps track of the total cost, IE cost_so_far + manhattan distance to end, for each point
	prev = {}						#This dictionary keeps track fo the previous for a particular point

	start_pos = Position(start, 0)				#Add the start to the priority queue
	p_queue.put(start_pos)
	prev[start] = None
	cost_so_far[start] = 0
	cost[start] = 0

	while not p_queue.empty():
		opened += 1									
		current = p_queue.get()				#Remove an item from the priority queue
		x_pos = current.pos[0]
		y_pos = current.pos[1]
 
		if x_pos == end[0] and y_pos == end[1]:
			break

		neighbors = [(x_pos -1, y_pos), (x_pos, y_pos + 1), (x_pos + 1, y_pos), (x_pos, y_pos - 1)]

		for neighbor in neighbors:			#Consider each of the four neighbors of the current point
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):		#Cant go out of bounds of the maze
				if not walls[neighbor[0]][neighbor[1]]:		#Can't go into a wall
					if neighbor not in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)):	#Make sure you either havn't looked at a position yet, or the cost to get to that position by following the current path is less than by following the path that is currently set for that positon
						new = Position(neighbor, cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end))		#Create a new Position object for the neighbor
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + 1	
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new)			#Put the neighbor in the queue

	path = copy.deepcopy(maze)
	current = end
	while maze[current[0]][current[1]] != 'P':				#Generate the path from the start to then end, and write it on the maze list
		current = prev[(current[0], current[1])]
		path[current[0]][current[1]] = '.'

	path[start[0]][start[1]] = 'P'

	return path, cost_so_far[end], opened
	


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

	path, cost, opened = a_star(maze, (4, 1), (4, 4), walls)
	for line in path:
		print(line)

	print(cost)
	print(opened)
