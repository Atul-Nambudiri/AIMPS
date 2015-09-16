from bfs import bfs
from dfs import dfs

def main():
	maze = []
	walls = []
	start = []
	end = []
	with open('mediumMaze.txt', 'r') as mazeText:
		lines = [x.strip('\r\n') for x in mazeText.readlines()]
		for i in range(len(lines)):
			toInsertToMaze = []
			toInsertToWalls = []
			for j in range(len(lines[i])):
				char = lines[i][j]
				toInsertToMaze.append(char)
				if char == '.':
					start = [i, j]
				elif char == 'P':
					end = [i, j]
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

	#print("BFS:")
	#resp = bfs(maze, start, end, walls)
	#print(resp)

	#print("DFS:")
	#resp = dfs(maze, start, end, walls)
	#for row in resp:
	#	print(row)

if __name__ == "__main__":
	main()
	