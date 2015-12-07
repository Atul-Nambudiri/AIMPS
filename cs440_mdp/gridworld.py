import sys
import copy
import math

reward_map = [[-.04,-1.0,-.04,-.04,-.04,-.04],
			  [-.04,-.04,-.04,"W",-1.0,-.04],
			  [-.04,-.04,-.04,"W",-.04,3.0],
			  [-.04,-.04,-.04,"W",-.04,-.04],
			  [-.04,-.04,-.04,-.04,-.04,-.04],
			  [1.0,-1.0,-.04,"W",-1.0,-1.0]]

"""Part A"""

utility_map_prev_a = [[0.0,-1.0,0.0,0.0,0.0,0.0],
				      [0.0,0.0,0.0,"W",-1.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,3.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,0.0,0.0,0.0],
				      [1.0,-1.0,0.0,"W",-1.0,-1.0]]

utility_map_new_a =  [[0.0,-1.0,0.0,0.0,0.0,0.0],
				      [0.0,0.0,0.0,"W",-1.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,3.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,0.0,0.0,0.0],
				      [1.0,-1.0,0.0,"W",-1.0,-1.0]]

policy_map_a = [["U",-1.0,"U","U","U","U"],
			    ["U","U","U","W","U","U"],
			    ["U","U","U","W","U",3.0],
			    ["U","U","U","W","U","U"],
			    ["U","U","U","U","U","U"],
			    [1.0,-1.0,"U","W",-1.0,-1.0]]

converg_flag_a = False

"""Part B"""

utility_map_prev_b = [[0.0,0.0,0.0,0.0,0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,0.0,0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0]]

utility_map_new_b =  [[0.0,0.0,0.0,0.0,0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0],
				      [0.0,0.0,0.0,0.0,0.0,0.0],
				      [0.0,0.0,0.0,"W",0.0,0.0]]

policy_map_b = [["U","U","U","U","U","U"],
			    ["U","U","U","W","U","U"],
			    ["U","U","U","W","U","U"],
			    ["U","U","U","W","U","U"],
			    ["U","U","U","U","U","U"],
			    ["U","U","U","W","U","U"]]

converg_flag_b = False

""" Value Iteration: Ui+s(s) = R(s) + gamma * max(submation(P(s'|s,a)Ui(s)))"""

def calcUltility_a():
	global utility_map_prev_a
	global utility_map_new_a
	global converg_flag_a
	global policy_map_a
	curr_max = -1000000.0
	temp_max = 0.0
	converg_count = 0
	transition_up = 0.8
	transition_left = 0.1
	transition_right = 0.1
	gamma = 0.99
	counter = 0

	for i in range(len(reward_map)):
		for j in range(len(reward_map[0])):
			curr_max = -1000000.0

			if (i == 0 and j == 1) or (i == 1 and (j == 3 or j == 4)) or (i == 2 and (j == 3 or j == 5)) or (i == 3 and j == 3) or (i == 5 and (j == 3 or j == 0 or j == 1 or j == 4 or j == 5)):
				converg_count += 1
				continue

			"""Up"""
			temp_max = 0.0 
			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_up * utility_map_prev_a[i-1][j]
			else:
				temp_max += transition_up * utility_map_prev_a[i][j]

			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_left * utility_map_prev_a[i][j-1]
			else:
				temp_max += transition_left * utility_map_prev_a[i][j]

			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_right * utility_map_prev_a[i][j+1]
			else:
				temp_max += transition_right * utility_map_prev_a[i][j]

			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_a[i][j] = "U"

			"""Right"""
			temp_max = 0.0
			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_up * utility_map_prev_a[i][j+1]
			else:
				temp_max += transition_up * utility_map_prev_a[i][j]

			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_left * utility_map_prev_a[i-1][j]
			else:
				temp_max += transition_left * utility_map_prev_a[i][j]

			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_right * utility_map_prev_a[i+1][j]
			else:
				temp_max += transition_right * utility_map_prev_a[i][j]
			
			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_a[i][j] = "R"

			"""Down"""
			temp_max = 0.0
			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_up * utility_map_prev_a[i+1][j]
			else:
				temp_max += transition_up * utility_map_prev_a[i][j]

			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_left * utility_map_prev_a[i][j+1]
			else:
				temp_max += transition_left * utility_map_prev_a[i][j]

			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_right * utility_map_prev_a[i][j-1]
			else:
				temp_max += transition_right * utility_map_prev_a[i][j]
			
			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_a[i][j] = "D"

			"""Left"""
			temp_max = 0.0
			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_up * utility_map_prev_a[i][j-1]
			else:
				temp_max += transition_up * utility_map_prev_a[i][j]

			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_left * utility_map_prev_a[i+1][j]
			else:
				temp_max += transition_left * utility_map_prev_a[i][j]	

			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_right * utility_map_prev_a[i-1][j]
			else:
				temp_max += transition_right * utility_map_prev_a[i][j]

			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_a[i][j] = "L"

			utility_map_new_a[i][j] = reward_map[i][j] + (gamma * curr_max)

			if abs(utility_map_new_a[i][j] - utility_map_prev_a[i][j]) < .1:
				converg_count += 1

	for a in range(len(utility_map_prev_a)):
		for b in range(len(utility_map_prev_a[0])):
			utility_map_prev_a[a][b] = utility_map_new_a[a][b]

	if converg_count == (len(reward_map) * len(reward_map[0])):
		converg_flag_a = True 


def calcUltility_b():
	global utility_map_prev_b
	global utility_map_new_b
	global converg_flag_b
	global policy_map_b
	curr_max = -1000000.0
	temp_max = 0.0
	converg_count = 0
	transition_up = 0.8
	transition_left = 0.1
	transition_right = 0.1
	gamma = 0.99
	counter = 0

	for i in range(len(reward_map)):
		for j in range(len(reward_map[0])):
			curr_max = -1000000.0

			if (i == 1 and j == 3) or (i == 2 and j == 3) or (i == 3 and j == 3) or (i == 5 and j == 3):
				converg_count += 1
				continue

			"""Up"""
			temp_max = 0.0 
			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_up * utility_map_prev_b[i-1][j]
			else:
				temp_max += transition_up * utility_map_prev_b[i][j]

			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_left * utility_map_prev_b[i][j-1]
			else:
				temp_max += transition_left * utility_map_prev_b[i][j]

			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_right * utility_map_prev_b[i][j+1]
			else:
				temp_max += transition_right * utility_map_prev_b[i][j]

			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_b[i][j] = "U"

			"""Right"""
			temp_max = 0.0
			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_up * utility_map_prev_b[i][j+1]
			else:
				temp_max += transition_up * utility_map_prev_b[i][j]

			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_left * utility_map_prev_b[i-1][j]
			else:
				temp_max += transition_left * utility_map_prev_b[i][j]

			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_right * utility_map_prev_b[i+1][j]
			else:
				temp_max += transition_right * utility_map_prev_b[i][j]
			
			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_b[i][j] = "R"

			"""Down"""
			temp_max = 0.0
			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_up * utility_map_prev_b[i+1][j]
			else:
				temp_max += transition_up * utility_map_prev_b[i][j]

			if ((j+1) < 6) and (reward_map[i][j+1] != "W"):
				temp_max += transition_left * utility_map_prev_b[i][j+1]
			else:
				temp_max += transition_left * utility_map_prev_b[i][j]

			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_right * utility_map_prev_b[i][j-1]
			else:
				temp_max += transition_right * utility_map_prev_b[i][j]
			
			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_b[i][j] = "D"

			"""Left"""
			temp_max = 0.0
			if ((j-1) >= 0) and (reward_map[i][j-1] != "W"):
				temp_max += transition_up * utility_map_prev_b[i][j-1]
			else:
				temp_max += transition_up * utility_map_prev_b[i][j]

			if ((i+1) < 6) and (reward_map[i+1][j] != "W"):
				temp_max += transition_left * utility_map_prev_b[i+1][j]
			else:
				temp_max += transition_left * utility_map_prev_b[i][j]	

			if ((i-1) >= 0) and (reward_map[i-1][j] != "W"):
				temp_max += transition_right * utility_map_prev_b[i-1][j]
			else:
				temp_max += transition_right * utility_map_prev_b[i][j]

			if temp_max > curr_max:
				curr_max = temp_max
				policy_map_b[i][j] = "L"

			utility_map_new_b[i][j] = reward_map[i][j] + (gamma * curr_max)

			if abs(utility_map_new_b[i][j] - utility_map_prev_b[i][j]) < .00001:
				converg_count += 1

	for a in range(len(utility_map_prev_b)):
		for b in range(len(utility_map_prev_b[0])):
			utility_map_prev_b[a][b] = utility_map_new_b[a][b]

	if converg_count == (len(reward_map) * len(reward_map[0])):
		converg_flag_b = True 


def main():
	global converg_flag_a
	loop_count_a = 0
	loop_count_b = 0

	"""Part A"""
	while not(converg_flag_a):
		loop_count_a += 1
		calcUltility_a()

	print("Iterations:" + str(loop_count_a))

	for a in range(len(utility_map_new_a)):
		print utility_map_new_a[a]

	print("")

	for b in range(len(policy_map_a)):
		print policy_map_a[b]

	print("")

	"""Part B"""
	while not(converg_flag_b):
		loop_count_b += 1
		calcUltility_b()

	print("Iterations:" + str(loop_count_b))

	for a in range(len(utility_map_new_b)):
		print utility_map_new_b[a]

	print("")

	for b in range(len(policy_map_b)):
		print policy_map_b[b]

main()
