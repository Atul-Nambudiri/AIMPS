import sys
import copy
import math

reward_map = [[-.04,-1.0,-.04,-.04,-.04,-.04],
			  [-.04,-.04,-.04,"W",-1.0,-.04],
			  [-.04,-.04,-.04,"W",-.04,3.0],
			  [-.04,-.04,-.04,"W",-.04,-.04],
			  [-.04,-.04,-.04,-.04,-.04,-.04],
			  [1.0,-1.0,-.04,"W",-1.0,-1.0]]

utility_map_prev = [[0.0,-1.0,0.0,0.0,0.0,0.0],
				    [0.0,0.0,0.0,"W",-1.0,0.0],
				    [0.0,0.0,0.0,"W",0.0,3.0],
				    [0.0,0.0,0.0,"W",0.0,0.0],
				    [0.0,0.0,0.0,0.0,0.0,0.0],
				    [1.0,-1.0,0.0,"W",-1.0,-1.0]]

utility_map_new =  [[0.0,-1.0,0.0,0.0,0.0,0.0],
				    [0.0,0.0,0.0,"W",-1.0,0.0],
				    [0.0,0.0,0.0,"W",0.0,3.0],
				    [0.0,0.0,0.0,"W",0.0,0.0],
				    [0.0,0.0,0.0,0.0,0.0,0.0],
				    [1.0,-1.0,0.0,"W",-1.0,-1.0]]

converg_flag = False

""" Value Iteration: Ui+s(s) = R(s) + gamma * max(submation(P(s'|s,a)Ui(s)))"""

def calcUltility():
	global utility_map_prev
	global utility_map_new
	global converg_flag
	curr_max = 0.0
	temp_max = 0.0
	converg_count = 0
	transition_up = 0.8
	transition_left = 0.1
	transition_right = 0.1
	gamma = 0.7

	for i in range(len(reward_map)):
		for j in range(len(reward_map[0])):
			# if reward_map[i][j] != -.04: 
			# 	converg_count += 1
			# 	continue

			if (i == 0 and j == 1) or (i == 1 and (j == 3 or j == 4)) or (i == 2 and (j == 3 or j == 5)) or (i == 3 and j == 3) or (i == 5 and (j == 3 or j == 0 or j == 1 or j == 4 or j == 5)):
				converg_count += 1
				continue

			# if (i == 1 and j == 3) or (i == 2 and j == 3) or (i == 3 and j == 3) or (i == 5 and j == 3):
			# 	converg_count += 1
			# 	continue

			"""Up"""
			temp_max = 0.0 
			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_up * utility_map_prev[i-1][j]
			else:
				temp_max += transition_up * utility_map_prev[i][j]

			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_left * utility_map_prev[i][j-1]
			else:
				temp_max += transition_left * utility_map_prev[i][j]

			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_right * utility_map_prev[i][j+1]
			else:
				temp_max += transition_right * utility_map_prev[i][j]

			if temp_max > curr_max:
				curr_max = temp_max

			"""Right"""
			temp_max = 0.0
			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_up * utility_map_prev[i][j+1]
			else:
				temp_max += transition_up * utility_map_prev[i][j]

			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_left * utility_map_prev[i-1][j]
			else:
				temp_max += transition_left * utility_map_prev[i][j]

			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_right * utility_map_prev[i+1][j]
			else:
				temp_max += transition_right * utility_map_prev[i][j]
			
			if temp_max > curr_max:
				curr_max = temp_max

			"""Down"""
			temp_max = 0.0
			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_up * utility_map_prev[i+1][j]
			else:
				temp_max += transition_up * utility_map_prev[i][j]

			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_left * utility_map_prev[i][j+1]
			else:
				temp_max += transition_left * utility_map_prev[i][j]

			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_right * utility_map_prev[i][j-1]
			else:
				temp_max += transition_right * utility_map_prev[i][j]
			
			if temp_max > curr_max:
				curr_max = temp_max

			"""Left"""
			temp_max = 0.0
			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_up * utility_map_prev[i][j-1]
			else:
				temp_max += transition_up * utility_map_prev[i][j]

			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_left * utility_map_prev[i+1][j]
			else:
				temp_max += transition_left * utility_map_prev[i][j]	

			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_right * utility_map_prev[i-1][j]
			else:
				temp_max += transition_right * utility_map_prev[i][j]

			if temp_max > curr_max:
				curr_max = temp_max


			utility_map_new[i][j] = reward_map[i][j] + (gamma * curr_max)
			#print utility_map_new[i][converg_flag]

			if abs(utility_map_new[i][j] - utility_map_prev[i][j]) < .00001:
				converg_count += 1
			# else:
			# 	print(str(i) + "," + str(j))

	for a in range(len(utility_map_prev)):
		for b in range(len(utility_map_prev[0])):
			utility_map_prev[a][b] = utility_map_new[a][b]

	if converg_count == (len(reward_map) * len(reward_map[0])):
		converg_flag = True 



	#print converg_count 


def main():
	global converg_flag
	loop_count = 0
	# calcUltility()
	# print("\n")
	# calcUltility()
	# calcUltility()
	# calcUltility()
	while not(converg_flag):
		loop_count += 1
		calcUltility()
		# print("\n")
	print loop_count

	for a in range(len(utility_map_new)):
		print utility_map_new[a]

main()