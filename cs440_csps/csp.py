import sys
import copy
import re

def solvePuzzleWords(array, words, locations):
	if len(locations.keys()) is 0:
		if 0 not in array and array not in solutions:
			solutions.append(array)
			print("solution: " + str(array))
			return

	else:
		for elem in words[locations.keys()[0]]:
			broken = False
			newList = copy.deepcopy(array)
			for j in range(len(locations[locations.keys()[0]])):
				if newList[locations[locations.keys()[0]][j] - 1] is 0:
					newList[locations[locations.keys()[0]][j] - 1] = elem[j]
				else:
					if newList[locations[locations.keys()[0]][j] - 1] is not elem[j]:
						broken = True
						break

			if not broken:
				modLocations = copy.deepcopy(locations)
				del modLocations[locations.keys()[0]]
				solvePuzzleWords(newList, words, modLocations)

		return


def solvePuzzleLetters(array, words, locations):
	if len(locations.keys()) is 0:
		if 0 not in array and array not in solutions:
			solutions.append(array)
			print("solution: " + str(array))
			return
	else:
		for elem in words[locations.keys()[0]]:
			for j in range(len(locations[locations.keys()[0]])):
				newList = copy.deepcopy(array)
				if newList[locations[locations.keys()[0]][j] - 1] is 0:
					newList[locations[locations.keys()[0]][j] - 1] = elem[j]
					modLocations = copy.deepcopy(locations)
					del modLocations[locations.keys()[0]]
					solvePuzzleLetters(newList, words, modLocations)
					array = copy.deepcopy(newList)
				else:
					if newList[locations[locations.keys()[0]][j] - 1] is elem[j]:
						modLocations = copy.deepcopy(locations)
						del modLocations[locations.keys()[0]]
						solvePuzzleLetters(newList, words, modLocations)

		return


def main():
	locations = {}
	words = {}

	length = 0

	with open('puzzle1.txt','r') as locationsfile:
		lines = [x.strip('\r\n') for x in locationsfile.readlines()]
		for i in range(len(lines)):
			if i is 0:
				length = int(lines[i])
			else:
				tempIndex = lines[i].index(':')
				tempString = lines[i][tempIndex + 2:]
				l = tempString.split(", ")
				for j in range(len(l)):
					l[j] = int(l[j])
				locations[lines[i][:tempIndex]] = l

	with open('wordslist.txt', 'r') as wordsfile:
		lines = [x.strip('\r\n') for x in wordsfile.readlines()]
		for i in range(len(lines)):
			tempIndex = lines[i].index(':')
			tempString = lines[i][tempIndex + 2:]
			l = tempString.split(", ")
			words[lines[i][:tempIndex]] = l

	array = [0 for x in range(length)]
	
	# solvePuzzleWords(array, words, locations)
	solvePuzzleLetters(array, words, locations)


cacheMoney = []
solutions = []
main()

for elem in cacheMoney:
	print(elem)