import sys
import copy
import time

blue = 0
green = 0

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

def recurseWrapper(board, scores, depth, original, person, opposite, minimax):
	best_score = 0
	best_pos = None
	if not minimax:
		best_score = 100000000
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				board[i][j] = person
				modified.append((i, j))
				modified.append("")
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < 6 and neighbors[t][1] < 6:
						if board[neighbors[t][0]][neighbors[t][1]] == opposite:
							modified.append(neighbors[t])
							modified.append(board[neighbors[t][0]][neighbors[t][1]])
							board[neighbors[t][0]][neighbors[t][1]] = person
				score = recurse(board, scores, depth - 1, original, opposite, person, not minimax)
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

def recurse(board, scores, depth, original, person, opposite, minimax):
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
		return score_board(scores, board, original)
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				modifiedPrev = []
				board[i][j] == person
				modified.append((i, j))
				modified.append("")
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < 6 and neighbors[t][1] < 6:
						if board[neighbors[t][0]][neighbors[t][1]] == opposite:
							modified.append(neighbors[t])
							modified.append(board[neighbors[t][0]][neighbors[t][1]])
							board[neighbors[t][0]][neighbors[t][1]] = person
				score = recurse(board, scores, depth - 1, original, opposite, person, not minimax)
				if minimax:
					if score > best_score:
						best_score = score
				else:
					if score < best_score:
						best_score = score
				for t in range(0, len(modified), 2):
					board[modified[t][0]][modified[t][1]] = modified[t+1]
	if not found:			#If you can no longer make any moves but have not gotten to the end of the recursion depth
		return score_board(scores, board, original)
	return best_score


def alphabetaWrapper(board, scores, depth, original, person, opposite, minimax):
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
				board[i][j] = person
				modified.append((i, j))
				modified.append("")
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < 6 and neighbors[t][1] < 6:
						if board[neighbors[t][0]][neighbors[t][1]] == opposite:
							modified.append(neighbors[t])
							modified.append(board[neighbors[t][0]][neighbors[t][1]])
							board[neighbors[t][0]][neighbors[t][1]] = person
				score = alphabeta(board, scores, depth - 1, original, opposite, person, not minimax, alpha, beta)
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

def alphabeta(board, scores, depth, original, person, opposite, minimax, alpha, beta):
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
		#print("scoring - %d" % score_board(scores, board, original))
		return score_board(scores, board, original)
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == "":
				found = 1
				modified = []
				modifiedPrev = []
				board[i][j] == person
				modified.append((i, j))
				modified.append("")
				neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
				for t in range(len(neighbors)):
					if neighbors[t][0] >= 0 and neighbors[t][1] >= 0 and neighbors[t][0] < 6 and neighbors[t][1] < 6:
						if board[neighbors[t][0]][neighbors[t][1]] == opposite:
							modified.append(neighbors[t])
							modified.append(board[neighbors[t][0]][neighbors[t][1]])
							board[neighbors[t][0]][neighbors[t][1]] = person
				score = alphabeta(board, scores, depth - 1, original, opposite, person, not minimax, alpha, beta)
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
		return score_board(scores, board, original)
	return best_score


def runner(function1, function2, depth1, depth2):
	global blue
	global green
	green = 0
	blue = 0
	times = []
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
		char = current
		if current == "G":
			startTime = time.time()
			score, pos = function1(board, scores, depth1, current, current, opposite, True)
			times.append(time.time() - startTime)
		else:
			startTime = time.time()
			score, pos = function2(board, scores, depth2, current, current, opposite, True)
			times.append(time.time() - startTime)
		board[pos[0]][pos[1]] = char
		neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
		for neighbor in neighbors:
			if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < 6 and neighbor[1] < 6:
				if board[neighbor[0]][neighbor[1]] == opposite:
					board[neighbor[0]][neighbor[1]] = char
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
	print("Average number of nodes expanded per move: %d" % ((blue + green)/36))
	print("Green Expanded %d Nodes" % green)
	print("Blue Expanded %d Nodes" % blue)
	print("Average Time per move: %f" % (sum(times)/36))


def main():
	if len(sys.argv) < 2:
		print("Must Enter in a Map")
	else:
		print("Run on board: %s" % sys.argv[1])
		print("Maximum found depth for Minimax: 3")
		print("Maximum found depth for Alphabeta: 5")
		print("Minimax vs Minimax - Depth 3 vs 3")
		runner(recurseWrapper, recurseWrapper, 3, 3)
		print("")
		print("Minimax vs Alphabeta - Depth 3 vs 5")
		runner(recurseWrapper, alphabetaWrapper, 3, 5)
		print("")
		print("Alphabeta vs Minimax - Depth 5 vs 3")
		runner(alphabetaWrapper, recurseWrapper, 5, 3)
		print("")
		print("Alphabeta vs Alphabeta - Depth 5 vs 5")
		runner(alphabetaWrapper, alphabetaWrapper, 5, 5)
		print("")
		print("Minimax vs Alphabeta - Depth 3 vs 3")
		runner(recurseWrapper, alphabetaWrapper, 3, 3)
		print("")
		print("Alphabeta vs Minimax - Depth 3 vs 3")
		runner(alphabetaWrapper, recurseWrapper, 3, 3)
		print("")
		print("Alphabeta vs Alphabeta - Depth 3 vs 3")
		runner(alphabetaWrapper, alphabetaWrapper, 3, 3)	




if __name__ == "__main__":
	main()


