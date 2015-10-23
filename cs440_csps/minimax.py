import sys
import copy

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
			print(move)
			print("Before")
			for line in board:
				print(line)
			char = current
			score, pos = recurseWrapper(board, scores, 3, current, current, opposite, True)
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
			print("After")
			for line in board:
				print(line)
			move -= 1
		for line in scores:
			print(line)



if __name__ == "__main__":
	main()


