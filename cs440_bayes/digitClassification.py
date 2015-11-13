import sys
import copy
import math

def main():
	labelDict = {}
	imageDict = {}
	numberTest = []
	numberTrain = []
	pClass = {}
	trainingDict0 = {}
	trainingDict1 = {}
	testingDict = {}
	postTestDict = {}

	###initialize a labelDict to have the indices and the total count of the indices ie {1: 50}###
	##this makes it easy to calculate pClass###
	with open('traininglabels', 'r') as labels:
		numberTrain = [x.strip('\r\n') for x in labels.readlines()]
		for i in range(len(numberTrain)):
			if numberTrain[i] not in labelDict:
				labelDict[numberTrain[i]] =  1
			else:
				labelDict[numberTrain[i]] = labelDict[numberTrain[i]] + 1

	###initialize a dictionary to contain images mapped to whatever value it corresponds to###
	with open('trainingimages', 'r') as images:
		img = [x.strip('\r\n') for x in images.readlines()]
		idxTr = 0
		for i in range(len(img)):
			if i % 28 == 0:
				if numberTrain[idxTr] not in imageDict:
					imageDict[numberTrain[idxTr]] = []
					image = []
					for j in range(28):
						image.append([])
						for k in range(28):
							image[j].append(img[i + j][k])

					imageDict[numberTrain[idxTr]].append(image)
				else:
					image = []
					for j in range(28):
						image.append([])
						for k in range(28):
							image[j].append(img[i + j][k])

					imageDict[numberTrain[idxTr]].append(image)
			
				idxTr = idxTr + 1

	###calculate P(class) for all integers 0 - 9###
	for i in labelDict.keys():
		pClass[i] = float(labelDict[i])/float(len(numberTrain))


	##run training for every key in imageDict to get an average image in trainingDict1 and trainingDict0###
	for key in imageDict.keys():
		training(key, imageDict, trainingDict0, trainingDict1)

	with open('testlabels', 'r') as labels:
		numberTest = [x.strip('\r\n') for x in labels.readlines()]

	###initialize a dictionary to contain images mapped to whatever value it corresponds to###
	with open('testimages', 'r') as images:
		img = [x.strip('\r\n') for x in images.readlines()]
		idxTr = 0
		for i in range(len(img)):
			if i % 28 == 0:
				if numberTest[idxTr] not in testingDict:
					testingDict[numberTest[idxTr]] = []
					image = []
					for j in range(28):
						image.append([])
						for k in range(28):
							image[j].append(img[i + j][k])

					testingDict[numberTest[idxTr]].append(image)
				else:
					image = []
					for j in range(28):
						image.append([])
						for k in range(28):
							image[j].append(img[i + j][k])

					testingDict[numberTest[idxTr]].append(image)
			
				idxTr = idxTr + 1

	###run testing to make a postTestDict###
	for key in testingDict.keys():
		postTestDict[key] = []
		testing(key, testingDict, trainingDict0, trainingDict1, pClass, postTestDict)

	###evaluate evaluate to get a confusionMatrix###
	confusionMatrix = evaluate(postTestDict)
	
	###calculate the oddsRatios###
	oddsRatios(confusionMatrix, trainingDict0, trainingDict1)

###calculate training by P(Fij = f | class) = ###
###(number of times pixel (i,j) has value f in training examples from this class) / ###
###(Total # of training examples from this class).###
def training(key, imageDict, trainingDict0, trainingDict1):
	probMap0 = []
	for i in range(28):
		probMap0.append([])
		for j in range(28):
			probMap0[i].append(0)

	probMap1 = []
	for i in range(28):
		probMap1.append([])
		for j in range(28):
			probMap1[i].append(0)


	for i in range(len(probMap0)):
		for j in range(len(probMap0[i])):
			numF0 = 0
			numF1 = 0
			for image in imageDict[key]:
				if image[i][j] == "+" or image[i][j] == "#":
					numF1 += 1
				else:
					numF0 += 1

			#V is set to a va;lue of 2 because you have 0 through 1 and k is a value arbitrarily chosen###
			###in this case, 1 was best because it limits the number of variance between the denominator and numerator from the actual value###
			k = 1
			probMap1[i][j] = float(numF1 + k) / float(len(imageDict[key]) + (k * 2))
			probMap0[i][j] = float(numF0 + k) / float(len(imageDict[key]) + (k * 2))

	trainingDict1[key] = probMap1
	trainingDict0[key] = probMap0

###testing which is calculated as###
###log P(class) + log P(f1,1 | class) + log P(f1,2 | class) + ... + log P(f28,28 | class)###
def testing(key, testingDict, trainingDict0, trainingDict1, pClass, postTestDict):
	for image in testingDict[key]:
		d = {}
		for dictKey in testingDict.keys():
			logSum = math.log(pClass[key])
			for i in range(28):
				for j in range(28):
					if image[i][j] == "+" or image[i][j] == "#":
						logSum = logSum + math.log(trainingDict1[dictKey][i][j])
					else:
						logSum = logSum + math.log(trainingDict0[dictKey][i][j])

			d[dictKey] = logSum

		postTestDict[key].append(d)


###evaluate a confusionMatrix by taking the max of every value that you've gotten from training###
def evaluate(postTestDict):
	confusionMatrix = []
	for i in range(10):
		confusionMatrix.append([])
		for j in range(10):
			confusionMatrix[i].append(0)

	keysList = [int(key) for key in postTestDict.keys()]
	keysList.sort()

	for key in keysList:
		for i in range(len(postTestDict[str(key)])):
		 	max = -10000000
		 	k = -1
		 	for j in postTestDict[str(key)][i].keys():
		 		if max < postTestDict[str(key)][i][j]:
		 			k = j
		 			max = postTestDict[str(key)][i][j]

		 	confusionMatrix[key][int(k)] = confusionMatrix[key][int(k)] + 1

	for i in range(10):
		l = len(postTestDict[str(i)])
		for j in range(10):
			confusionMatrix[i][j] = float(confusionMatrix[i][j])/float(l)

	return confusionMatrix

###calculate the oddsRatios###
def oddsRatios(confusionMatrix, trainingDict0, trainingDict1):
	l = [[[0, 0], 0] for x in range(4)]
	for i in range(10):
		for j in range(10):
			if i != j:
				for k in range(4):
					if l[k][1] < confusionMatrix[i][j]:
						l[k][0] = [i, j]
						l[k][1] = confusionMatrix[i][j]
						break

	for i in range(4):
		first = copy.deepcopy(trainingDict1[str(l[i][0][0])])
		second = copy.deepcopy(trainingDict1[str(l[i][0][1])])
		third = copy.deepcopy(trainingDict1[str(l[i][0][0])])
		
		for j in range(len(first)):
			for k in range(len(first[j])):
				a = first[j][k]
				b = second[j][k]

				first[j][k] = math.log(a)
				second[j][k] = math.log(b)
				third[j][k] = math.log(a/b)

		for j in range(len(first)):
			for k in range(len(first[j])):
				if first[j][k] < 1 and first[j][k] > -1:
					first[j][k] = "8"
				elif first[j][k] >= 1:
					first[j][k] = " "
				else:
					first[j][k] = " "


				if second[j][k] < 1 and second[j][k] > -1:
					second[j][k] = "8"
				elif second[j][k] >= 1:
					second[j][k] = " "
				else:
					second[j][k] = " "

		for j in range(len(third)):
			for k in range(len(third[j])):
				if third[j][k] < 1.1 and third[j][k] >= 0.9:
					third[j][k] = " "
				elif third[j][k] >= 1.1 or (third[j][k] < 0.9 and third[j][k] >= 0):
					third[j][k] = "+"
				else:
					third[j][k] = "-"

		for line in third:
			print("".join(line))

		print(" ")

main()