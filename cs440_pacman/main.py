from bfs import bfs
from dfs import dfs
from a_star import a_star
from a_star12 import a_star12
from greedy import greedy
from a_star13 import a_star13

def main():
	maze = []
	walls = []
	start = ()
	end = ()
	with open('smallGhost.txt', 'r') as mazeText:
		lines = [x.strip('\r\n') for x in mazeText.readlines()]
		for i in range(len(lines)):
			toInsertToMaze = []
			toInsertToWalls = []
			for j in range(len(lines[i])):
				char = lines[i][j]
				toInsertToMaze.append(char)
				if char == '.':
					end = (i, j)
				elif char == 'P':
					start = (i, j)
				if char == '.' or char == 'P' or char == ' ' or char == 'g' or char == 'G':
					toInsertToWalls.append(False)
				else:
					toInsertToWalls.append(True)
			maze.append(toInsertToMaze)
			walls.append(toInsertToWalls)
	
	# for i in maze:
	# 	print i
# """

# 	for i in walls:
# 		print i"""

	#print(start)
	#print(end)

	# '''i = 0
	# results = a_star12(maze, start, end, walls)
	# for item in results:
	# 	for line in item[0]:
	# 		print(line)

	# 	file_name = "output%d" % i
	# 	with open(file_name, 'w') as out:
	# 		for line in item[0]:
	# 			output_line = "".join(line)
	# 			out.write("%s\n" % output_line)

	# 	i += 1

	# 	print("Cost: %s" % (item[1]))
	# 	print("Nodes Visited: %s" % (item[2]))
	# '''

	path, steps, opened = a_star13(maze, start, end, walls)
	for line in path:
		print(line)

	print(steps)
	print(opened)

	
	with open('output', 'w') as out:
		for line in path:
			output_line = "".join(line)
			out.write("%s\n" % output_line) 



if __name__ == "__main__":
	main()
	