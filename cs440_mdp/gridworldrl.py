import sys
import copy
import math
import random

reward_map = [[-.04, -1.0, -.04, -.04, -.04, -.04],
			  [-.04, -.04, -.04,  "W", -1.0, -.04],
			  [-.04, -.04, -.04,  "W", -.04,  3.0],
			  [-.04, -.04, -.04,  "W", -.04, -.04],
			  [-.04, -.04, -.04, -.04, -.04, -.04],
			  [ 1.0, -1.0, -.04,  "W", -1.0, -1.0]]

def exploration_function(q, n):
	"""
	The exploration function to use to find the desired action
	"""
	if n < 5:
		return 0.1
	else:
		return q

def chosenDir():
	"""
	Based upon the given probabilities, gives the probability that you go in the direction you chose, or left, or right from your intended direction
	"""
	my_list = [-1] * 10 + [1] * 10 + [0] * 80
	return random.choice(my_list)


def successorState(i, j, dir):
	"""
	Finds the successor state of the current states given the action dir you have chosen to go in
	"""
	wanted = chosenDir()
	if dir == 0:
		if wanted == 0:
			return (i -1, j)
		elif wanted == -1:
			return (i, j - 1)
		else:
			return (i, j + 1)
	elif dir == 1:
		if wanted == 0:
			return (i, j+1)
		elif wanted == -1:
			return (i-1, j)
		else:
			return (i+1, j)
	elif dir == 2:
		if wanted == 0:
			return (i + 1, j)
		elif wanted == -1:
			return (i, j + 1)
		else:
			return (i, j - 1)
	else:
		if wanted == 0:
			return (i, j-1)
		elif wanted == -1:
			return (i+1, j)
		else:
			return (i-1, j)

def calcUltility():
	Q_prev = [[[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 	  [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 	  [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 	  [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 	  [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 	  [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]]]

	Q = [[[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]],
		 [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]]]
	N = [[[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]],
		 [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]],
		 [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]],
		 [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]],
		 [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]],
		 [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]]
	done = False
	v = 0.0
	while not done:
	#for v in range(5500):
		for i in range(len(reward_map)):
			for j in range(len(reward_map[0])):
				if reward_map[i][j] == "W":
					for t in range(4):
						Q[i][j][t] = 0.0
				elif reward_map[i][j] != -.04:
					for t in range(4):
						Q[i][j][t] = reward_map[i][j]
				else:
					bestScore = -100000000
					bestA = -1
					for t in range(4):
						curr = exploration_function(Q_prev[i][j][t], N[i][j][t])
						if curr > bestScore:
							bestScore = curr
							bestA = t
					# if i == 2 and j == 4:
					# 	for t in range(4):
					# 		print(exploration_function(Q_prev[i][j][t], N[i][j][t]))
					# 	print("BestScore: %f BestDir: %d" % (bestScore, bestA))
					N[i][j][bestA] += 1
					nextState = successorState(i, j, bestA)
					# if i == 2 and j == 4:
					# 	print(nextState)
					if ((nextState[0] >= len(N) or nextState[1] >= len(N[0]) or nextState[0] < 0 or nextState[1] < 0) or reward_map[nextState[0]][nextState[1]] == "W"):
						nextState = (i, j)
					bestNextState = max(Q_prev[nextState[0]][nextState[1]])
					alpha = 60.0/(59.0 + v)
					# if i == 2 and j == 4:
					# 	print("Alpha: " + str(alpha))
					# 	print("Prev: " + str(Q_prev[i][j][bestA]))
					# 	print(Q_prev[i][j][bestA] + alpha * (reward_map[i][j] + .99 * bestNextState - Q_prev[i][j][bestA]))
					Q[i][j][bestA] = Q_prev[i][j][bestA] + alpha * (reward_map[i][j] + .99 * bestNextState - Q_prev[i][j][bestA])
		v += 1.0
		number = 0
		for i in range(len(Q)):
			for j in range(len(Q[0])):
				for k in range(len(Q[0][0])):
					if abs(Q_prev[i][j][k] - Q[i][j][k]) < 0.0010:
						number += 1
					Q_prev[i][j][k] = Q[i][j][k]
		if number == 144:
			done = True

	print("Took %f Iterations" % v)
	print("")
	for row in Q:
		print([max(item) for item in row])
	print("")
	for row in N:
		print(row)


calcUltility()