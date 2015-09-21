from bfs import bfs
from dfs import dfs

def main():
	maze = []
	walls = []
	start = ()
	end = ()
	with open('mediumMaze.txt', 'r') as mazeText:
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
				if char == '.' or char == 'P' or char == ' ':
					toInsertToWalls.append(False)
				else:
					toInsertToWalls.append(True)
			maze.append(toInsertToMaze)
			walls.append(toInsertToWalls)
	
	for i in maze:
		print i

	for i in walls:
		print i

	print(start)
	print(end)

if __name__ == "__main__":
	main()
	