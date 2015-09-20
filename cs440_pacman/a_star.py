import copy
import math
from position import Position
from Queue import PriorityQueue

def manhattan_distance(current, dest):
	return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

def a_star(maze, start, end, walls):
	opened = 0
	p_queue = PriorityQueue(maxsize=0)
	visited = copy.deepcopy(walls)

	cost_so_far = {}
	cost = {}
	prev = {}

	start_pos = Position(start, 0)
	p_queue.put(start_pos)
	prev[start] = None
	cost_so_far[start] = 0
	cost[start] = 0

	while not p_queue.empty():
		opened += 1
		current = p_queue.get()
		x_pos = current.pos[0]
		y_pos = current.pos[1]
		visited[x_pos][y_pos] = True
 
		if x_pos == end[0] and y_pos == end[1]:
			break

		neighbors = [(x_pos -1, y_pos), (x_pos, y_pos + 1), (x_pos + 1, y_pos), (x_pos, y_pos - 1)]

		for neighbor in neighbors:
			if not neighbor[0] < 0 and not neighbor[1] < 0 and not neighbor[0] >= len(visited) and not neighbor[1] >= len(visited[0]):
				if not visited[neighbor[0]][neighbor[1]]:
					if neighbor not in cost or cost[neighbor] > (cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)):
						new = Position(neighbor, cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end))
						cost_so_far[new.pos] = cost_so_far[(x_pos, y_pos)] + 1
						cost[new.pos] = cost_so_far[(x_pos, y_pos)] + 1 + manhattan_distance(neighbor, end)
						prev[new.pos] = [x_pos, y_pos]
						p_queue.put(new)

	path = copy.deepcopy(maze)
	current = end
	steps = 0
	while maze[current[0]][current[1]] != '.':
		current = prev[(current[0], current[1])]
		path[current[0]][current[1]] = '.'
		steps += 1

	return path, steps, opened
	


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

	path, steps, opened = a_star(maze, (4, 1), (4, 4), walls)
	for line in path:
		print(line)

	print(steps)
	print(opened)