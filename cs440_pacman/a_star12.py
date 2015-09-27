import copy
import math
from position import Position
from Queue import PriorityQueue

def manhattan_distance(current, dest, straight, turn, direction_facing):
	"""
	This function calculates the manhattan distance from the current point to the destination
	"""
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

def new(current, dest, straight, turn, direction_facing):
	"""
	This function calculates the new heuristic distance from the current point to the destination. It is an extension of the manhattan distance. 
	However, the varied costs for turns and going straight are taken into account. We calculate the minimum number of turns that are required to 
	reach the end of the maze, and the minmum number of times we have to go straight. We then mulitply both of these values by their respective multipliers. 
	We then return this value.
	"""
	change_x = math.fabs(current[0] - dest[0])		#Calculate the total number of times we have to go straight
	change_y =  math.fabs(current[1] - dest[1])
	num_turns = 0
	if direction_facing == 1:				#Calculate the number of turns we have to take when facing different directions
		if dest[0] - current[0] > 0:
			num_turns +=  2
		if dest[1] != current[1]:
			num_turns += 1
	if direction_facing == 3:
		if dest[0] - current[0] < 0:
			num_turns +=  2
		if dest[1] != current[1]:
			num_turns += 1
	if direction_facing == 2:
		if dest[1] - current[1] < 0:
			num_turns +=  2
		if dest[1] != current[1]:
			num_turns += 1
	if direction_facing == 4:
		if dest[1] - current[1] > 0:
			num_turns +=  2
		if dest[1] != current[1]:
			num_turns += 1

	return (change_x + change_y) * straight + turn * num_turns	#Multiply by the costs

def a_star12(maze, start, end, walls):
	"""
	This returns an array with the results of runnning a_star with the two heurstics, with the two different sets of costs
	"""
	return [a_star(maze, start, end , walls, manhattan_distance, 1, 2), a_star(maze, start, end , walls, manhattan_distance, 2, 1), a_star(maze, start, end , walls, new, 1, 2), a_star(maze, start, end , walls, new, 2, 1)]

def a_star(maze, start, end, walls, distance_function, straight, turn):
	"""
	Runs a_star with the passed in distance formula, and costs for going straight and turning
	"""
	opened = 0
	p_queue = PriorityQueue(maxsize=0)			#Use a priority queue to get the position with the highest priority

	cost_so_far = {}					#This dictionary keeps track of the cost of the total number of steps taken to reach a particular point
	cost = {}						#This dicitonary keeps track of the total cost, IE cost_so_far + distance to end, for each point 

	prev = {}						#This dictionary keeps track of the previous for a particular point
	direction_facing = {}					#This dictionary keeps track of th edirection that you are facing at any point. 
	
	start_pos = Position(start, 0)				#Add start to the priority queue
	p_queue.put(start_pos)
	prev[start] = None
	cost_so_far[start] = 0
	cost[start] = 0
	direction_facing[start] = 1

	while not p_queue.empty():
		opened += 1
		current = p_queue.get()				#Remove the item with the highest priority from the queue
		x_pos = current.pos[0]
		y_pos = current.pos[1]
		cur_dir = direction_facing[current.pos]

		if x_pos == end[0] and y_pos == end[1]:
			break

		neighbors = {(x_pos -1, y_pos) : 1, (x_pos, y_pos + 1) : 2, (x_pos + 1, y_pos) : 3, (x_pos, y_pos - 1) : 4}			#Keeps track of all the four neighbors from the current point, along witht he direction you would be facing if you go to that point

		for neighbor, new_dir in neighbors.iteritems():		#Consider each of the four neighbors
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):			#Can't go out of bounds of the maze
				if not walls[neighbor[0]][neighbor[1]]:		#Can't go into a wall
					extra_cost = 0		#This calculates th cost of moving in the new direction, based upon the passed in costs for going straight and turning, and the number of turns needed to move in a new direction
					if new_dir == cur_dir:	
						extra_cost = straight
					elif math.fabs(new_dir - cur_dir) % 2 == 0:
						extra_cost = 2 * turn + straight
					else:
						extra_cost = straight + turn
					if neighbor not in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + extra_cost + distance_function(neighbor, end, straight, turn, new_dir)): #Make sure you either haven't looked at a position yet, or the cost to get to that position by followign the current path is less then by following the path that is currently set for that position
						new = Position(neighbor, cost_so_far[(x_pos, y_pos)] + extra_cost + distance_function(neighbor, end, straight, turn, new_dir))		#Create a new position object for the neighbor.
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + extra_cost
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + extra_cost + distance_function(neighbor, end, straight, turn, new_dir)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new)	#Put the neighbor in the p_queue
						direction_facing[neighbor] = new_dir

	path = copy.deepcopy(maze)
	current = end
	while maze[current[0]][current[1]] != 'P':		#Generate the path from the start to the end, and write it on the maze list
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

	path, steps, opened = a_star(maze, (4, 4), (4, 1), walls, manhattan_distance, 1, 0)
	for line in path:
		print(line)

	print(steps)
	print(opened)
