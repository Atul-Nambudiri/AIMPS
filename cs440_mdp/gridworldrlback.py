import sys
import copy
import math
import random
import Queue
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

# reward_map = [[-.04,-.04,-.04,"W",-.04, 1.0],
# 			  [-.04,"W",-.04,"W",-.04,-.04],
# 			  [-.04,"W",-.04,-.04,-.04,-.04],
# 			  [-.04,"W",-.04,-.04,-.04,-.04],
# 			  [-.04,-.04,-.04,-1.0,-.04,-1.0],
# 			  [-.04,-.04,-1.0,-1.0,-.04,1.0]]

# terminal = [[0, 0, 0, 1, 0, 1],
# 		  	[0, 1, 0, 1, 0, 0],
# 		  	[0, 1, 0, 0, 0, 0],
# 		  	[0, 1, 0, 0, 0, 0],
# 		  	[0, 0, 0, 1, 0, 1],
# 		  	[0, 0, 1, 1, 0, 1]]

# actual = [[-0.0893, -1, 0.1235, 0.2727, 0.4901, 1.0104],  
# 		  [0.0481, -0.0012, 0.0313, 0, -1, 1.6882],  
# 		  [0.1515, 0.0594, 0.0162,0, 1.6514, 3], 
# 		  [0.3156, 0.1565, 0.0909,0, 1.1625, 1.8509],  
# 		  [0.5760, 0.2235, 0.2029, 0.4219, 0.7193, 1.1257],  
# 		  [1,-1, 0.0039, 0, -1, -1]]  

actual = [[1.6651416839325817, -1.0, 1.8121583727070574, 1.8358641736662824, 1.9095493274026687, 2.347858515145151],
		  [2.070393878387167, 2.1400379454100604, 2.2097851202975796, 0.0, -1.0, 2.4827968923418426],
		  [2.138730427225045, 2.2177756751892144, 2.2970353417105374, 0.0, 2.743906336587694, 3.0],
		  [2.1966223740843622, 2.2904253569624453, 2.386504472753691, 0.0, 2.7970451596064008, 2.9000082698759035],
		  [2.131322648441104, 2.230355027842207, 2.4791734200266484, 2.629345807310131, 2.7130502862286865, 2.8028839579562494],
		  [1.0, -1.0, 2.024970348550524, 0.0, -1.0, -1.0]]

# actual = [[0.430847208601019, 0.49374950274382484, 0.5505019886643367, 0.0, 0.9309002863458881, 1.0],
# 		  [0.3755143224453596, 0.0, 0.6150579731572945, 0.0, 0.8761733131278144, 0.9309002863458881],
# 		  [0.32077662819628483, 0.0, 0.6733308107831529, 0.7459213905139961, 0.8132366787947167, 0.8632446753253965],
# 		  [0.26652617689822455, 0.0, 0.622939606638047, 0.6867864931514681, 0.750971480379035, 0.7969322128947233],
# 		  [0.25211584089767886, 0.3115988883587278, 0.385194456061422, -1.0, 0.4633475647708057, -1.0],
# 		  [0.19422336511511465, 0.15979956151243627, -1.0, -1.0, 0.8855398545086477, 1.0]]

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

def calcUtility(Ne, Rp, alphaNum):
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
	known_reward_map = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			  			[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			  			[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			  			[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			  			[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
			  			[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

	explored = [[0, 1, 0, 0, 0, 0],
		  		[0, 0, 0, 1, 1, 0],
		  		[0, 0, 0, 1, 0, 1],
		  		[0, 0, 0, 1, 0, 0],
		  		[0, 0, 0, 0, 0, 0],
		  		[1, 1, 0, 1, 1, 1]]
	done = False
	v = 0.0
	while not done:
		i = 3
		j = 1
		v += 1.0
		while True:
			explored[i][j] = 1
			if terminal[i][j] == 1:
				for t in range(4):
					Q[i][j][t] = reward_map[i][j]
				break
			else:
				bestScore = -100000000
				bestA = -1
				for t in range(4):
					curr = exploration_function(Q[i][j][t], N[i][j][t], Ne, Rp)
					if curr > bestScore:
						bestScore = curr
						bestA = t
				best = []
				for t in range(4):
					if exploration_function(Q[i][j][t], N[i][j][t], Ne, Rp) == bestScore:
						best.append(t)
				bestA = random.choice(best)
				N[i][j][bestA] += 1
				nextState = successorState(i, j, bestA)
				if ((nextState[0] >= len(N) or nextState[1] >= len(N[0]) or nextState[0] < 0 or nextState[1] < 0) or reward_map[nextState[0]][nextState[1]] == "W"):
					nextState = (i, j)
				bestNextState = max(Q[nextState[0]][nextState[1]])
				alpha = alphaNum/((alphaNum-1) + v)
				Q[i][j][bestA] = (Q[i][j][bestA] + alpha * (reward_map[i][j] + (0.99 * bestNextState) - Q[i][j][bestA]))
				i = nextState[0]
				j = nextState[1]
		number = 0
		explored_num = 06
		#print("V: %f" % v)
		for l in range(len(Q)):
			#print([max(t) for t in Q[l]])
			for m in range(len(Q[0])):
				if explored[l][m] == 1:
					explored_num += 1
				for n in range(4):
					if v > 1500.0:
						if abs(Q_prev[l][m][n] - Q[l][m][n]) < 0.0001:
							number += 1
						Q_prev[l][m][n] = Q[l][m][n]
			if number == 144: #and explored_num == 36:
				done = True 
	#print("V: %f" % v)
	res = []
	for i in range(len(Q)):
		res.append([max(item) for item in Q[i]])
	return res

def runCalcUtility(Ne, Rp, alpha):
	policy  = [[0, 0, 0, 0, 0, 0],
	  		   [0, 0, 0, 1, 0, 0],
			   [0, 0, 0, 1, 0, 0],
	  		   [0, 0, 0, 1, 0, 0],
	  		   [0, 0, 0, 0, 0, 0],
	  		   [0, 0, 0, 1, 0, 0]]
	print("Calculating Utility with Ne of %d, and Rp of %f, and alpha of %d" % (Ne, Rp, alpha))
	res = calcUtility(Ne, Rp, float(alpha))
	num = 1
	for t in range(num - 1):
		Q = calcUtility(Ne, Rp, float(alpha))
		for i in range(len(Q)):
			for j in range(len(Q[0])):
				res[i][j] += Q[i][j]
	for i in range(len(res)):
		for j in range(len(res[0])):
			res[i][j] /= num
	summation = 0
	for i in range(len(res)):
		for j in range(len(res[0])):
			summation += (res[i][j] - actual[i][j])**2
		print([item for item in res[i]])
	print("")
	rme = (summation/36)**(0.5)
	print("RMSE: %f" % rme)
	return (rme, (Ne, Rp, alpha))

queue = Queue.PriorityQueue()
bestValue = 1
bestNe = -1
bestRp = -1.0
bestAlpha = -1

def addToQueue(result):
	global queue
	global bestValue
	global bestNe
	global bestRp
	global bestAlpha
	if result[0] < bestValue:
		bestValue = result[0]
		bestNe = result[1][0]
		bestRp = result[1][1]
		bestAlpha = result[1][2]
	print("Best rme so far was found at Ne %d, Rp %f, alpha %d  with value %f" % (bestNe, bestRp, bestAlpha, bestValue))
	queue.put(result)


def main():
	global queue
	global bestValue
	global bestN
	global bestRp
	global bestAlpha
	args = []
	for alpha in range(7000, 7001, 1000):
		for Ne in range(0, 7001, 1000):
			for Rp in range (0, 5, 1):
				args.append((Ne, Rp, alpha))
	pool = Pool()
	for i in args:
		pool.apply_async(runCalcUtility, args = i, callback = addToQueue)
	pool.close()
	pool.join()
	#print("Best rme was found at Ne %d, Rp %f, alpha %d  with value %f" % (bestNe, bestRp, bestAlpha, bestValue))	
	print("All values in queue")
	while not queue5empty():
		print(queue.get())

def main2():
	args = [(3000, 3, 3000)] #, (1500, 3, 60), (5, 3, 30000), (1500, 3, 30000), (5, 30000, 60), (2700, 5, 2700), (3700, 5, 3700), (4700, 5, 4700), (100, 5, 100)]
	pool = Pool()
	for i in args:
		pool.apply_async(runCalcUtility, args = i, callback = addToQueue)
	pool.close()
	pool.join()
	#print("Best rme was found at Ne %d, Rp %f, alpha %d  with value %f" % (bestNe, bestRp, bestAlpha, bestValue))	
	print("All values in queue")
	while not queue.empty():
		print(queue.get())

main2()