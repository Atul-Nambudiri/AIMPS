import sys
import copy
import time

blue = 0
green = 0
ratioScoringAlgorithm = False

def score_board(scores, pieces, player):
	"""
	Looks through all the pieces and finds the score for green and blue
	"""
	score = 0
	for i in range(len(pieces)):
		for j in range(len(pieces[0])):
			if pieces[i][j] == player:
				score += scores[i][j]
	return score

def recurseWrapper(board, scores, depth, original, opponent, person, opposite, minimax):
	"""
	A wrapper around the recurse function for minimax search that returns the best position.
	"""
	best_score = 0
	best_pos = None
	if not minimax:
		best_score = 100000000
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				canBlitz = 0
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
						if board[neighbors[t][0]][neighbors[t][1]] == person:
							canBlitz = 1
				if canBlitz:
					for t in range(len(neighbors)):
						if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
							if board[neighbors[t][0]][neighbors[t][1]] == opposite:
								modified.append(neighbors[t])
								modified.append(board[neighbors[t][0]][neighbors[t][1]])
								board[neighbors[t][0]][neighbors[t][1]] = person
				board[i][j] = person
				modified.append((i, j))
				modified.append("")
				score = recurse(board, scores, depth - 1, original, opponent, opposite, person, not minimax)
				if minimax:
					if score > best_score:
						best_score = score
						best_pos = (i, j)
				else:
					if score < best_score:
						best_score = score
						best_pos = (i, j)
				for t in range(0, len(modified), 2):
					board[modified[t][0]][modified[t][1]] = modified[t+1]
	return best_score, best_pos

def recurse(board, scores, depth, original, opponent, person, opposite, minimax):
	"""
	A function that runs minimax search and returns the best score at the particular min/max level
	"""
	global green
	global blue
	if original == 'G':
		green += 1
	else:
		blue += 1
	best_score = 0
	if not minimax:
		best_score = 100000000
	found = 0
	if depth == 0:
		if ratioScoringAlgorithm:
			return float(score_board(scores, board, original))/max(1.0, float(score_board(scores, board, opponent)))
		else:
			return (score_board(scores, board, original))
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				canBlitz = 0
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
						if board[neighbors[t][0]][neighbors[t][1]] == person:
							canBlitz = 1
				if canBlitz:
					for t in range(len(neighbors)):
						if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
							if board[neighbors[t][0]][neighbors[t][1]] == opposite:
								modified.append(neighbors[t])
								modified.append(board[neighbors[t][0]][neighbors[t][1]])
								board[neighbors[t][0]][neighbors[t][1]] = person
				board[i][j] = person
				modified.append((i, j))
				modified.append("")
				score = recurse(board, scores, depth - 1, original, opponent, opposite, person, not minimax)
				if minimax:
					if score > best_score:
						best_score = score
				else:
					if score < best_score:
						best_score = score
				for t in range(0, len(modified), 2):
					board[modified[t][0]][modified[t][1]] = modified[t+1]
	if not found:			#If you can no longer make any moves but have not gotten to the end of the recursion depth
		if ratioScoringAlgorithm:
			return float(score_board(scores, board, original))/max(1.0, float(score_board(scores, board, opponent)))
		else:
			return (score_board(scores, board, original))
	return best_score


def alphabetaWrapper(board, scores, depth, original, opponent, person, opposite, minimax):
	"""
	A wrapper around the recurse function for alphabeta pruning search that returns the best position.
	"""
	alpha = -10000000000000
	beta = 100000000000000
	best_score = 0
	best_pos = None
	if not minimax:
		best_score = 100000000
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				canBlitz = 0
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
						if board[neighbors[t][0]][neighbors[t][1]] == person:
							canBlitz = 1
				if canBlitz:
					for t in range(len(neighbors)):
						if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
							if board[neighbors[t][0]][neighbors[t][1]] == opposite:
								modified.append(neighbors[t])
								modified.append(board[neighbors[t][0]][neighbors[t][1]])
								board[neighbors[t][0]][neighbors[t][1]] = person
				board[i][j] = person
				modified.append((i, j))
				modified.append("")
				score = alphabeta(board, scores, depth - 1, original, opponent, opposite, person, not minimax, alpha, beta)
				if minimax:
					if score > best_score:
						best_score = score
						best_pos = (i, j)
						alpha = max(alpha, best_score)
				else:
					if score < best_score:
						best_score = score
						best_pos = (i, j)
						beta = min(beta, best_score)
				for t in range(0, len(modified), 2):
					board[modified[t][0]][modified[t][1]] = modified[t+1]
	return best_score, best_pos

def alphabeta(board, scores, depth, original, opponent, person, opposite, minimax, alpha, beta):
	"""
	A function that runs alphabeta pruning search and returns the best score at the particular min/max level
	"""
	global green
	global blue
	if original == 'G':
		green += 1
	else:
		blue += 1
	best_score = 0
	if not minimax:
		best_score = 100000000
	found = 0
	if depth == 0:
		if ratioScoringAlgorithm:
			return float(score_board(scores, board, original))/max(1.0, float(score_board(scores, board, opponent)))
		else:
			return (score_board(scores, board, original))
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				canBlitz = 0
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
						if board[neighbors[t][0]][neighbors[t][1]] == person:
							canBlitz = 1
				if canBlitz:
					for t in range(len(neighbors)):
						if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
							if board[neighbors[t][0]][neighbors[t][1]] == opposite:
								modified.append(neighbors[t])
								modified.append(board[neighbors[t][0]][neighbors[t][1]])
								board[neighbors[t][0]][neighbors[t][1]] = person
				board[i][j] = person
				modified.append((i, j))
				modified.append("")
				score = alphabeta(board, scores, depth - 1, original, opponent, opposite, person, not minimax, alpha, beta)
				for t in range(0, len(modified), 2):
					board[modified[t][0]][modified[t][1]] = modified[t+1]
				if minimax:
					if score > best_score:
						best_score = score
						if best_score >= beta:
							return best_score
						alpha = max(alpha, best_score)
				else:
					if score < best_score:
						best_score = score
						if best_score <= alpha:
							return best_score
						beta = min(beta, best_score)
	if not found:			#If you can no longer make any moves but have not gotten to the end of the recursion depth
		if ratioScoringAlgorithm:
			return float(score_board(scores, board, original))/max(1.0, float(score_board(scores, board, opponent)))
		else:
			return (score_board(scores, board, original))
	return best_score


def alphabetaBetterWrapper(board, scores, depth, original, opponent, person, opposite, minimax):
	"""
	A wrapper around the recurse function for alphabeta pruning search that returns the best position.
	This version uses a more efficient ordering that will cause more pruning.
	"""
	alpha = -10000000000000
	beta = 100000000000000
	best_score = 0
	best_pos = None
	if not minimax:
		best_score = 100000000
	changing = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				changed = scores[i][j]
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				canBlitz = 0
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
						if board[neighbors[t][0]][neighbors[t][1]] == person:
							canBlitz = 1
				if canBlitz:
					for t in range(len(neighbors)):
						if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
							changed += scores[neighbors[t][0]][neighbors[t][0]]
				changing.append(((i, j), changed))
	changing.sort(key=lambda x: x[1])
	if minimax:
		changing.reverse()
	for item in changing:
		i = item[0][0]
		j = item[0][1]
		found = 1
		modified = []
		neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
		canBlitz = 0
		for t in range(len(neighbors)):
			if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
				if board[neighbors[t][0]][neighbors[t][1]] == person:
					canBlitz = 1
		if canBlitz:
			for t in range(len(neighbors)):
				if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
					if board[neighbors[t][0]][neighbors[t][1]] == opposite:
						modified.append(neighbors[t])
						modified.append(board[neighbors[t][0]][neighbors[t][1]])
						board[neighbors[t][0]][neighbors[t][1]] = person
		board[i][j] = person
		modified.append((i, j))
		modified.append("")
		score = alphabetaBetter(board, scores, depth - 1, original, opponent, opposite, person, not minimax, alpha, beta)
		if minimax:
			if score > best_score:
				best_score = score
				best_pos = (i, j)
				alpha = max(alpha, best_score)
		else:
			if score < best_score:
				best_score = score
				best_pos = (i, j)
				beta = min(beta, best_score)
		for t in range(0, len(modified), 2):
			board[modified[t][0]][modified[t][1]] = modified[t+1]
	return best_score, best_pos

def alphabetaBetter(board, scores, depth, original, opponent, person, opposite, minimax, alpha, beta):
	"""
	A function that runs alphabeta pruning search and returns the best score at the particular min/max level. 
	This version uses a more efficient ordering that will cause more pruning
	"""
	global green
	global blue
	if original == 'G':
		green += 1
	else:
		blue += 1
	best_score = 0
	if not minimax:
		best_score = 100000000
	found = 0
	if depth == 0:
		if ratioScoringAlgorithm:
			return float(score_board(scores, board, original))/max(1.0, float(score_board(scores, board, opponent)))
		else:
			return (score_board(scores, board, original))
	changing = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				changed = scores[i][j]
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				canBlitz = 0
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
						if board[neighbors[t][0]][neighbors[t][1]] == person:
							canBlitz = 1
				if canBlitz:
					for t in range(len(neighbors)):
						if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
							changed += scores[neighbors[t][0]][neighbors[t][0]]
				changing.append(((i, j), changed))
	changing.sort(key=lambda x: x[1])
	if minimax:
		changing.reverse()
	for item in changing:
		i = item[0][0]
		j = item[0][1]
		found = 1
		modified = []
		neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
		canBlitz = 0
		for t in range(len(neighbors)):
			if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
				if board[neighbors[t][0]][neighbors[t][1]] == person:
					canBlitz = 1
		if canBlitz:
			for t in range(len(neighbors)):
				if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
					if board[neighbors[t][0]][neighbors[t][1]] == opposite:
						modified.append(neighbors[t])
						modified.append(board[neighbors[t][0]][neighbors[t][1]])
						board[neighbors[t][0]][neighbors[t][1]] = person
		board[i][j] = person
		modified.append((i, j))
		modified.append("")
		score = alphabetaBetter(board, scores, depth - 1, original, opponent, opposite, person, not minimax, alpha, beta)
		for t in range(0, len(modified), 2):
			board[modified[t][0]][modified[t][1]] = modified[t+1]
		if minimax:
			if score > best_score:
				best_score = score
				if best_score >= beta:
					return best_score
				alpha = max(alpha, best_score)
		else:
			if score < best_score:
				best_score = score
				if best_score <= alpha:
					return best_score
				beta = min(beta, best_score)
	if not found:			#If you can no longer make any moves but have not gotten to the end of the recursion depth
		if ratioScoringAlgorithm:
			return float(score_board(scores, board, original))/max(1.0, float(score_board(scores, board, opponent)))
		else:
			return (score_board(scores, board, original))
	return best_score


def runner(function1, function2, depth1, depth2):
	"""
	This function simulates a game between two AI's running the specified search functions
	"""
	global blue
	global green
	green = 0
	blue = 0
	green_times = []
	blue_times = []
	scores = []
	with open(sys.argv[1], 'r') as board_file:
		for line in board_file:
			linelist = line.replace('\t', " ").replace('\r\n', "").split(" ")
			linelist = [int(x) for x in linelist]
			scores.append(linelist)
	board = [["" for x in range(len(scores[0]))] for y in range(len(scores))]
	total_moves = (len(board)) * len(board[0])
	move = total_moves
	current = "G"
	opposite = "B"
	while move != 0:
		char = current
		if current == "G":
			startTime = time.time()
			score, pos = function1(board, scores, depth1, current, opposite, current, opposite, True)
			green_times.append(time.time() - startTime)
		else:
			startTime = time.time()
			score, pos = function2(board, scores, depth2, current, opposite, current, opposite, True)
			blue_times.append(time.time() - startTime)
		neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
		canBlitz = 0
		for t in range(len(neighbors)):
			if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
				if board[neighbors[t][0]][neighbors[t][1]] == char:
					canBlitz = 1
		if canBlitz:
			for neighbor in neighbors:
				if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < len(board) and neighbor[1] < len(board[0]):
					if board[neighbor[0]][neighbor[1]] == opposite:
						board[neighbor[0]][neighbor[1]] = char
		board[pos[0]][pos[1]] = char
		if current == "G":
			current = "B"
			opposite = "G"
		else:
			current = "G"
			opposite = "B"
		move -= 1
	print("Final Board:")
	for line in board:
		print(line)
	print("Green Score: %d" % score_board(scores, board, "G"))
	print("Blue Score: %d" % score_board(scores, board, "B"))
	print("Green Expanded %d Nodes Total" % green)
	print("Blue Expanded %d Nodes Total" % blue)
	print("Total average number of nodes expanded per move: %d" % ((blue + green)/total_moves))
	print("Green Expanded %d Nodes on Average" % (green/(total_moves/2)))
	print("Blue Expanded %d Nodes on Average" % (blue/(total_moves/2)))
	print("Total average Time per move: %f" % ((sum(blue_times) + sum(green_times))/total_moves))
	print("Average Time per move for Green: %f" % (sum(green_times)/(total_moves/2)))
	print("Average Time per move for Blue: %f" % (sum(blue_times)/(total_moves/2)))


def playerRunner(function, depth):
	"""
	This function allows you to play a game against an AI running the specified search function
	"""
	global blue
	global green
	blue = 0
	green = 0
	blue_times = []
	scores = []
	with open(sys.argv[1], 'r') as board_file:
		for line in board_file:
			linelist = line.replace('\t', " ").replace('\r\n', "").split(" ")
			linelist = [int(x) for x in linelist]
			scores.append(linelist)
	board = [["" for x in range(len(scores[0]))] for y in range(len(scores))]
	total_moves = (len(board)) * len(board[0])
	move = total_moves
	current = "B"
	while move != 0:
		print("Board:")
		for line in board: 
			print(line)
		print("Enter the x and y coordinates of where you want to play")
		xPos = input("X Coordinate:")
		yPos = input("Y Coordinate:")
		while xPos < 0 or yPos < 0 or xPos >= len(board) or yPos >= len(board[0]) or board[xPos][yPos] != "":
			print("Enter in valid x and y coordinates")
			xPos = input("X Coordinate:")
			yPos = input("Y Coordinate:")
		neighbors = [(xPos + 1, yPos), (xPos - 1, yPos), (xPos, yPos + 1), (xPos, yPos - 1)]
		canBlitz = 0
		for t in range(len(neighbors)):
			if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
				if board[neighbors[t][0]][neighbors[t][1]] == "G":
					canBlitz = 1
		if canBlitz:
			for neighbor in neighbors:
				if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < len(board) and neighbor[1] < len(board[0]):
					if board[neighbor[0]][neighbor[1]] == "B":
						board[neighbor[0]][neighbor[1]] = "G"
		board[xPos][yPos] = "G"
		move -= 1
		if move == 0:
			break
		startTime = time.time()
		score, pos = function(board, scores, depth, "B", "G", "B", "G", True)
		board[pos[0]][pos[1]] = "B"
		blue_times.append(time.time() - startTime)
		neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
		canBlitz = 0
		for t in range(len(neighbors)):
			if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < len(board) and neighbors[t][1] < len(board[0]):
				if board[neighbors[t][0]][neighbors[t][1]] == "B":
					canBlitz = 1
		if canBlitz:
			for neighbor in neighbors:
				if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < len(board) and neighbor[1] < len(board[0]):
					if board[neighbor[0]][neighbor[1]] == "G":
						board[neighbor[0]][neighbor[1]] = "B"
		move -= 1
	print("Final Board:")
	for line in board:
		print(line)
	print("Green Score: %d" % score_board(scores, board, "G"))
	print("Blue Score: %d" % score_board(scores, board, "B"))
	print("Blue Expanded %d Nodes Total" % blue)
	print("Blue Expanded %d Nodes on Average" % (blue/(total_moves/2)))
	print("Average Time per move for Blue: %f" % (sum(blue_times)/(total_moves/2)))

	


def main():
	"""
	The main executing function
	"""
	if len(sys.argv) == 3 and sys.argv[2] == 'player':
		print("User now playing against AI")
		playerRunner(recurseWrapper, 3)
		print("")
	elif len(sys.argv) < 2:
		print("Must Enter in a Map")
	else:
		print("Run on board: %s" % sys.argv[1])
		print("Maximum found depth for Minimax: 3")
		print("Maximum found depth for Alphabeta: 5")
		print("For all these maps, greem goes first, and blue goes second")
		# print("Minimax vs Minimax - Depth 3 vs 3")
		# runner(recurseWrapper, recurseWrapper, 3, 3)
		# print("")
		# print("Minimax vs Alphabeta - Depth 3 vs 3")
		# runner(recurseWrapper, alphabetaBetterWrapper, 3, 3)
		# print("")
		# print("Alphabeta vs Minimax - Depth 3 vs 3")
		# runner(alphabetaBetterWrapper, recurseWrapper, 3, 3)
		# print("")
		# print("Alphabeta vs Alphabeta - Depth 3 vs 3")
		# runner(alphabetaBetterWrapper, alphabetaBetterWrapper, 3, 3)
		# print("")
		# print("Minimax vs Normal Alphabeta - Depth 3 vs 5")
		# runner(recurseWrapper, alphabetaWrapper, 3, 5)
		# print("")
		# print("Normal Alphabeta vs Minimax - Depth 5 vs 3")
		# runner(alphabetaWrapper, recurseWrapper, 5, 3)
		# print("")
		# print("Normal Alphabeta vs Normal Alphabeta - Depth 5 vs 5")
		# runner(alphabetaWrapper, alphabetaWrapper, 5, 5)
		# print("")
		# print("Normal Alphabeta vs Normal Alphabeta - Depth 3 vs 5")
		# runner(alphabetaWrapper, alphabetaWrapper, 3, 5)
		# print("")
		# print("Minimax vs Enhanced Alphabeta - Depth 3 vs 3")
		# runner(recurseWrapper, alphabetaBetterWrapper, 3, 3)
		# print("")
		# print("Enhanced Alphabeta vs Minimax - Depth 3 vs 3")
		# runner(alphabetaBetterWrapper, recurseWrapper, 3, 3)
		# print("")
		print("Normal Alphabeta vs Enhanced Alphabeta - Depth 3 vs 3")
		runner(alphabetaWrapper, alphabetaBetterWrapper, 3, 3)
		print("")
		print("Enhanced Alphabeta vs Normal Alphabeta - Depth 3 vs 3")
		runner(alphabetaBetterWrapper, alphabetaWrapper, 3, 3)
		print("")
		print("Enhanced Alphabeta vs Enhanced Alphabeta - Depth 3 vs 3")
		runner(alphabetaBetterWrapper, alphabetaBetterWrapper, 3, 3)





if __name__ == "__main__":
	main()


