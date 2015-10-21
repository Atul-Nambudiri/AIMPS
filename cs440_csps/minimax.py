import sys 

def score(scores, pieces):
	"""
	Looks through all the pieces and finds the score for green and blue
	"""
	green = 0
	blue = 0
	for i in len(pieces)
		for j in len(pieces[0]):
			if pieces[i][j] == 'G':
				green += scores[i][j]
			elif pieces[i][j] == "B":
				blue += scores[i][j]
	return green, blue

def recurse(board, scores, depth, person, opposite, minimax):
	compare = max()
	best_score = 0
	best_pos = None
	if not minimax:
		compare = min()
		best_score = 100000000
	found = 0
	if depth == 0:
		return score(scores, board), None
	for i in len(board):
		for j in len(board[0]):
			if board[i][j] == "":
				found = 1
				modified = []
				board[i][j] == person
				modified.append((i, j))
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				for neighbor in neighbors:
					if board[neighbor[0]][neighbor[1]] == opposite:
						board[neighbor[0]][neighbor[1]] = person
				cost = recurse(board, scores, depth - 1, opposite, person, not minimax)
				cost = compare(cost, best_score)
				for item in modified:
					board[item[0][item[1]] = ""
	if not found:			#If you have reached the end of the maze but have not gotten to the end of the recursion depth
		return score(scores, board), None 
	return cost, best_pos


def main():
	if len(sys.argv) < 2:
		print("Must Enter in a Map")
	else:
		scores = []
		with open(sys.argv[1], 'r') as board_file:
			for line in board_file:
				linelist = line.replace('\t', " ").replace('\r\n', "").split(" ")
				linelist = [int(x) for x in linelist]
				scores.append(linelist)
		board = [["" for x in range(6)] for y in range(6)]
		move = 36
		current = "G"
		opposite = "B"
		while move != 0:
			pos = recurse(board, scores, 3, current, opposite, True)
			board[pos[0]][pos[1]] = current
			if current == "G":
				current = "B"
				opposite = "G"
			else:
				current = "G"
				opposite = "B"
			moves -= 1



if __name__ == "__main__":
	main()


