import copy
import math
from position import Position
from Queue import PriorityQueue

def manhattan_distance(current, dest, straight, turn, direction_facing):
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

def distance(current, dest, straight, turn, direction_facing):
	return math.sqrt(math.pow(math.fabs(current[0] - dest[0]), 2) + math.pow(math.fabs(current[1] - dest[1]), 2))

def new(current, dest, straight, turn, direction_facing):
	change_x = math.fabs(current[0] - dest[0])
	change_y =  math.fabs(current[1] - dest[1])
	num_turns = 0
	if direction_facing == 1:
		if dest[0] - current[0] > 0:
			num_turns +=  2
	if direction_facing == 3:
		if dest[0] - current[0] < 0:
			num_turns +=  2
	if direction_facing == 2:
		if dest[1] - current[1] < 0:
			num_turns +=  2
	if direction_facing == 4:
		if dest[1] - current[1] > 0:
			num_turns +=  2

	return (change_x + change_y) * straight + turn * num_turns

def a_star12(maze, start, end, walls):
	return [a_star(maze, start, end , walls, manhattan_distance, 1, 2), a_star(maze, start, end , walls, manhattan_distance, 2, 1), a_star(maze, start, end , walls, new, 1, 2), a_star(maze, start, end , walls, new, 2, 1)]

def a_star(maze, start, end, walls, distance_function, straight, turn):
	opened = 0
	p_queue = PriorityQueue(maxsize=0)

	cost_so_far = {}
	cost = {}
	prev = {}
	direction_facing = {}

	start_pos = Position(start, 0)
	p_queue.put(start_pos)
	prev[start] = None
	cost_so_far[start] = 0
	cost[start] = 0
	direction_facing[start] = 1

	while not p_queue.empty():
		opened += 1
		current = p_queue.get()
		x_pos = current.pos[0]
		y_pos = current.pos[1]
		cur_dir = direction_facing[current.pos]

		if x_pos == end[0] and y_pos == end[1]:
			break

		neighbors = {(x_pos -1, y_pos) : 1, (x_pos, y_pos + 1) : 2, (x_pos + 1, y_pos) : 3, (x_pos, y_pos - 1) : 4}

		for neighbor, new_dir in neighbors.iteritems():
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(walls) and not neighbor[1] >= len(walls[0]):
				if not walls[neighbor[0]][neighbor[1]]:
					extra_cost = 0
					if new_dir == cur_dir:
						extra_cost = straight
					elif math.fabs(new_dir - cur_dir) % 2 == 0:
						extra_cost = 2 * turn + straight
					else:
						extra_cost = straight + turn
					if neighbor not in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + extra_cost + distance_function(neighbor, end, straight, turn, new_dir)):
						new = Position(neighbor, cost_so_far[(x_pos, y_pos)] + extra_cost + distance_function(neighbor, end, straight, turn, new_dir))
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + extra_cost
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + extra_cost + distance_function(neighbor, end, straight, turn, new_dir)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new)
						direction_facing[neighbor] = new_dir

	path = copy.deepcopy(maze)
	current = end
	while maze[current[0]][current[1]] != 'P':
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
