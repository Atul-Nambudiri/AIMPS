import sys
import copy
import math

reward_map = [[-.04,-1,-.04,-.04,-.04,-.04],
			 [-.04,-.04,-.04,W,-1,-.04],
			 [-.04,-.04,-.04,W,-.04,3],
			 [-.04,-.04,-.04,W,-.04,-.04],
			 [-.04,-.04,-.04,-.04,-.04,-.04],
			 [1,-1,-.04,W,-1,-1]]

utility_map_prev = [[0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0]]

utility_map_new =  [[0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0],
				   [0,0,0,0,0,0]]

""" Value Iteration: Ui+s(s) = R(s) + gamma * max(submation(P(s'|s,a)Ui(s)))"""

def calcUltility():
	for i in range(len(reward_map)):
		for j in range(len(reward_map[0])):
			if 

def main():
	