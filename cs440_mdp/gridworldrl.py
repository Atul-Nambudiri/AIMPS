import sys
import copy
import math
import random
import Queue
import matplotlib.pyplot as plot
from multiprocessing import Pool

reward_map = [[-.04, -1.0, -.04, -.04, -.04, -.04],
			  [-.04, -.04, -.04,  "W", -1.0, -.04],
			  [-.04, -.04, -.04,  "W", -.04,  3.0],
			  [-.04, -.04, -.04,  "W", -.04, -.04],
			  [-.04, -.04, -.04, -.04, -.04, -.04],
			  [ 1.0, -1.0, -.04,  "W", -1.0, -1.0]]

terminal = [[0, 1, 0, 0, 0, 0],
		  	[0, 0, 0, 1, 1, 0],
		  	[0, 0, 0, 1, 0, 1],
		  	[0, 0, 0, 1, 0, 0],
		  	[0, 0, 0, 0, 0, 0],
		  	[1, 1, 0, 1, 1, 1]]

actual = [[1.6651416839325817, -1.0, 1.8121583727070574, 1.8358641736662824, 1.9095493274026687, 2.347858515145151],
		  [2.070393878387167, 2.1400379454100604, 2.2097851202975796, 0.0, -1.0, 2.4827968923418426],
		  [2.138730427225045, 2.2177756751892144, 2.2970353417105374, 0.0, 2.743906336587694, 3.0],
		  [2.1966223740843622, 2.2904253569624453, 2.386504472753691, 0.0, 2.7970451596064008, 2.9000082698759035],
		  [2.131322648441104, 2.230355027842207, 2.4791734200266484, 2.629345807310131, 2.7130502862286865, 2.8028839579562494],
		  [1.0, -1.0, 2.024970348550524, 0.0, -1.0, -1.0]]

action = {
	0 : "U",
	1 : "R",
	2 : "D",
	3 : "L"
}

def exploration_function(q, n, Ne, Rp):
	"""
	The exploration function to use to find the desired action
	"""
	if n < Ne:
		return Rp
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
		if wanted == 0:				#The wanted direction
			return (i -1, j)	
		elif wanted == -1:			#Right angle - Left
			return (i, j - 1)
		else:						#Right angle - Right
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

def calcUtility(Ne, Rp, alphaNum):
	"""
	This function runs the TD Q-learning algorithm on the maze
	"""
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
	items = []
	rmses = []
	utilities = []
	while not done:	#Loops until convergence occurs
		i = 3
		j = 1
		v += 1.0
		while True:	#Loops until a reward square is reached
			if terminal[i][j] == 1:			#Check is the square is a reward square
				for t in range(4):
					Q[i][j][t] = reward_map[i][j]
				break
			else:
				bestScore = -100000000
				bestA = -1
				for t in range(4):			#Run the exploration function of all the actions
					curr = exploration_function(Q[i][j][t], N[i][j][t], Ne, Rp)
					if curr > bestScore:
						bestScore = curr
						bestA = t
				best = []
				for t in range(4):
					if exploration_function(Q[i][j][t], N[i][j][t], Ne, Rp) == bestScore:
						best.append(t)
				bestA = random.choice(best)			#If there are duplicates, pick at random what we choose to do
				N[i][j][bestA] += 1
				nextState = successorState(i, j, bestA)
				if ((nextState[0] >= len(N) or nextState[1] >= len(N[0]) or nextState[0] < 0 or nextState[1] < 0) or reward_map[nextState[0]][nextState[1]] == "W"):
					nextState = (i, j)
				bestNextState = max(Q[nextState[0]][nextState[1]])
				alpha = alphaNum/((alphaNum-1) + v)			#Calculate the alpha
				Q[i][j][bestA] = (Q[i][j][bestA] + alpha * (reward_map[i][j] + (0.99 * bestNextState) - Q[i][j][bestA]))   #Update the Q value for the square using the TD learning method
				i = nextState[0]
				j = nextState[1]
		number = 0
		summation = 0
		subset = []
		for l in range(len(Q)):
			for m in range(len(Q[0])):
				if v % 20 == 0 and (l * 6 + m) % 5 == 0:	#Add utilites to graph eveyr 20 iterations
					subset.append(((l, m), max(Q[l][m])))
				summation += (max(Q[l][m]) - actual[l][m])**2
				for n in range(4):
					if v > 1500.0:
						if abs(Q_prev[l][m][n] - Q[l][m][n]) < 0.01:
							number += 1
						Q_prev[l][m][n] = Q[l][m][n]
		rmse = (summation/36)**(0.5)		#Calculate the rmse
		if number == 144:					#We have converged
			print("RMSE: %f" % rmse)
			done = True
		if v % 20 == 0:
			print(v)
			rmses.append(rmse)
			items.append(v)
			utilities.append(subset)
	plot.plot(items, rmses)			#Plot everything
	plot.xlabel('Trial')
	plot.ylabel('RMSE')
	plot.title('RMSE over tine')
	plot.show()
	plot.figure()
	for i in range(len(utilities[0])):
		print(i)
		plot.plot(items, [item[i][1] for item in utilities], label=str(utilities[0][i][0]))
	plot.xlabel("Trial")
	plot.ylabel("Utilities")
	plot.title('Utilities over time')
	plot.legend(loc='lower right', ncol=3, fancybox=True, shadow=True)
	plot.show()


	return Q

def runCalcUtility(Ne, Rp, alpha): 
	"""
	Runs the TD Q-learning algorithm, and prints out the final utilities and the policy
	"""
	policy  = [[0, 0, 0, 0, 0, 0],
	  		   [0, 0, 0, "W", 0, 0],
			   [0, 0, 0, "W", 0, 0],
	  		   [0, 0, 0, "W", 0, 0],
	  		   [0, 0, 0, 0, 0, 0],
	  		   [0, 0, 0, "W", 0, 0]]
	print("Calculating Utility with Ne of %d, and Rp of %f, and alpha of %d" % (Ne, Rp, alpha))
	res = calcUtility(Ne, Rp, float(alpha))
	summation = 0
	for i in range(len(res)):
		for j in range(len(res[0])):
			summation += (max(res[i][j]) - actual[i][j])**2
			bestScore = -10000000
			bestA = -1
			for t in range(4):
				if res[i][j][t] > bestScore:
					bestScore = res[i][j][t]
					bestA = t
			if reward_map[i][j] != "W":
				policy[i][j] = action[bestA]
		print([max(item) for item in res[i]])
	print("")
	for item in policy:
		print(item)
	rmse = (summation/36)**(0.5)
	print("Final RMSE: %f" % rmse)
	return (rmse, (Ne, Rp, alpha))

def main():
	runCalcUtility(3000, 3, 3000)

if __name__ == "__main__":
	main()