import sys
import copy
import re

def solvePuzzleWords(array, words, locations):
	if len(locations.keys()) is 0:
		if 0 not in array and array not in solutions:
			solutions.append(array)
			print("")
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
				print("")
				print(elem),
				print(" -> "),
				modLocations = copy.deepcopy(locations)
				del modLocations[locations.keys()[0]]
				solvePuzzleWords(newList, words, modLocations)

			if broken:
				print(elem),
				print(" -> bt"),
		return

def solvePuzzleLetters(array, locations, letterLocations, words, iterator):
	if len(letterLocations.keys()) == iterator:
		if 0 not in array and array not in solutions:
			#print(array)
			
			broken = False
			for key in locations.keys():
				s = ""
				for i in locations[key]:
					s += array[i - 1]

				if s not in words[key]:
					broken = True
					break

			if not broken:
				solutions.append(array)
				print("solution: " + str(array))
		return
	else:
		l = {}
		for elem in letterLocations[letterLocations.keys()[iterator]]:
			l[elem[0]] = []
			for word in words[elem[0]]:
				if word[elem[1]] not in l[elem[0]]:
					l[elem[0]].append(word[elem[1]])

		sharedLetters = []
		for char in l[l.keys()[0]]:
			inAllStrings = True
			if len(l.keys()) > 1:
				for i in range(1, len(l.keys())):
					if char not in l[l.keys()[i]]:
						inAllStrings = False
			
			if inAllStrings is True:
				sharedLetters.append(char)

		for letter in sharedLetters:
			newWords = copy.deepcopy(words)
			for elem in letterLocations[letterLocations.keys()[iterator]]:
				for word in newWords[elem[0]]:
					if word[elem[1]] is not letter:
						delIdx= newWords[elem[0]].index(word)
						del newWords[elem[0]][delIdx]

			newArray = copy.deepcopy(array)
			newArray[iterator] = letter
			solvePuzzleLetters(newArray, locations, letterLocations, newWords, iterator + 1)

		return

def main():
	locations = {}
	words = {}
	letterLocations = {}
	seenWords = {}
	length = 0

	with open('puzzle5.txt','r') as locationsfile:
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

	for elem in locations.keys():
		for i in range(len(locations[elem])):
			if locations[elem][i] in letterLocations:
				letterLocations[locations[elem][i]].append((elem, i))
			else:
				letterLocations[locations[elem][i]] = [(elem, i)]
	#print(letterLocations)

	array = [0 for x in range(length)]
	#solvePuzzleLetters(array, locations, letterLocations, words, 0)
	print(locations.keys())
	solvePuzzleWords(array, words, locations)

cacheMoney = []
solutions = []
main()

for elem in cacheMoney:
	print(elem)