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

	#print(pClass)

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

	for key in testingDict.keys():
		postTestDict[key] = []
		testing(key, testingDict, trainingDict0, trainingDict1, pClass, postTestDict)

	confusionMatrix = evaluate(postTestDict)
	# for line in confusionMatrix:
	# 	print(line)

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

			#V is set to a va;lue of 10 because you have 0 through 9 and k is a value of 
			k = 5
			probMap1[i][j] = float(numF1 + k) / float(len(imageDict[key]) + (k * 10))
			probMap0[i][j] = float(numF0 + k) / float(len(imageDict[key]) + (k * 10))

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

	for line in confusionMatrix:
		print(line)

main()