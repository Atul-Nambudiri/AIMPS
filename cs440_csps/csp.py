import sys
import copy
import re

def consistencyCheck(letterLocations, words):
	for key in letterLocations.keys():
		allLetters = {}

		if len(letterLocations[key]) > 1:
			for constraint in letterLocations[key]:
				allLetters[constraint[0]] = []
				for word in words[constraint[0]]:
					if word[constraint[1]] not in allLetters[constraint[0]]:
						allLetters[constraint[0]].append(word[constraint[1]])

			for char in allLetters[allLetters.keys()[0]]:
				for k,v in allLetters.iteritems():
					if char not in v:
						delIdx = allLetters[allLetters.keys()[0]].index(char)
						del allLetters[allLetters.keys()[0]][delIdx]
						break

			l = allLetters.keys()[0]
			for constraint in letterLocations[key]:
				for word in words[constraint[0]]:
					if word[constraint[1]] not in allLetters[l]:
						delIdx = words[constraint[0]].index(word)
						del words[constraint[0]][delIdx]

	for key in reversed(letterLocations.keys()):
		allLetters = {}

		if len(letterLocations[key]) > 1:
			for constraint in letterLocations[key]:
				allLetters[constraint[0]] = []
				for word in words[constraint[0]]:
					if word[constraint[1]] not in allLetters[constraint[0]]:
						allLetters[constraint[0]].append(word[constraint[1]])

			for char in allLetters[allLetters.keys()[0]]:
				for k,v in allLetters.iteritems():
					if char not in v:
						delIdx = allLetters[allLetters.keys()[0]].index(char)
						del allLetters[allLetters.keys()[0]][delIdx]
						break

			l = allLetters.keys()[0]
			for constraint in letterLocations[key]:
				for word in words[constraint[0]]:
					if word[constraint[1]] not in allLetters[l]:
						delIdx = words[constraint[0]].index(word)
						del words[constraint[0]][delIdx]

def consistencyCheck2(letterLocations, words):
	for key in letterLocations.keys():
		allLetters = {}

		if len(letterLocations[key]) > 1:
			for constraint in letterLocations[key]:
				allLetters[constraint[0]] = []
				for word in words[constraint[0]]:
					if word[constraint[1]] not in allLetters[constraint[0]]:
						allLetters[constraint[0]].append(word[constraint[1]])

			for char in allLetters[allLetters.keys()[0]]:
				for k,v in allLetters.iteritems():
					if char not in v:
						delIdx = allLetters[allLetters.keys()[0]].index(char)
						del allLetters[allLetters.keys()[0]][delIdx]
						break

			l = allLetters.keys()[0]
			for constraint in letterLocations[key]:
				for word in words[constraint[0]]:
					if word[constraint[1]] not in allLetters[l]:
						delIdx = words[constraint[0]].index(word)
						del words[constraint[0]][delIdx]

def solvePuzzleWords(array, words, letterLocations, locations, printList):
	if len(locations.keys()) is 0:
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
				print(printList)
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
			printList.append(elem)
			if not broken:
				print(printList) 

				modLocations = copy.deepcopy(locations)
				del modLocations[locations.keys()[0]]

				# modLetterLocations = copy.deepcopy(letterLocations)
				# del modLetterLocations[letterLocations.keys()[0]]
				# consistencyCheck2(modLetterLocations, words)

				solvePuzzleWords(newList, words, letterLocations, modLocations, printList)
				printList.pop()

			if broken:
				print(str(printList) + "BT")
				printList.pop()
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
			print(newArray[iterator])
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

	# for k, v in letterLocations.iteritems():
	# 	print(str(k) + ": " + str(v))

	# print("before")
	array = [0 for x in range(length)]
	
	for i in range(length):
		consistencyCheck(letterLocations, words)

	solvePuzzleLetters(array, locations, letterLocations, words, 0)
	#print(locations.keys())
	#solvePuzzleWords(array, words, letterLocations, locations, [])

cacheMoney = []
solutions = []
main()

for elem in cacheMoney:
	print(elem)