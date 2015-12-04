import sys
import copy
import math

def vectorSubtraction(list1, list2):
	if len(list1) != len(list2):
		return [-1]
	else:
		list3 = [0 for x in range(len(list1))]
		for i in range(len(list3)):
			list3[i] = list1[i] - list2[i]
		return list3

def vectorAddition(list1, list2):
	if len(list1) != len(list2):
		return [-1]
	else:
		list3 = [0 for x in range(len(list1))]
		for i in range(len(list3)):
			list3[i] = list1[i] + list2[i]
		return list3

def scalarProduct(scalingVal, list1):
	list2 = copy.deepcopy(list1)
	for i in range(len(list2)):
		list2[i] = list2[i] * scalingVal

	return list2

def dotProduct(list1, list2):
	if len(list1) != len(list2):
		return -1
	else:
		sum = 0
		for i in range(len(list1)):
			sum = sum + (list1[i] * list2[i])
		return sum

def main():
	trainingLabels = []
	trainingInstances = []
	testLabels = []
	testInstances = []
	weights = {}

	# occurences = {}

	with open('traininglabels', 'r') as labels:
		trainingLabels = [int(x.strip('\r\n')) for x in labels.readlines()]
		# for i in range(len(trainingLabels)):
		# 	if int(trainingLabels[i]) not in occurences:
		# 		occurences[int(trainingLabels[i])] =  1
		# 	else:
		# 		occurences[int(trainingLabels[i])] =  occurences[trainingLabels[i]] + 1

	with open('trainingimages', 'r') as images:
		img = [x.strip('\r\n') for x in images.readlines()]
		for i in range(len(img)):
			if i % 28 == 0:
				imageInstance = []
				for j in range(28):
					for k in range(28):
						if img[i+j][k] == "+" or img[i+j][k] == "#":
							imageInstance.append(1)
						else:
							imageInstance.append(0)
				trainingInstances.append(imageInstance)

	for i in range(10):
		weightInstance = []
		for j in range(784):
			#subject to change
			weightInstance.append(0)

		weights[i] = weightInstance

	perceptron(trainingLabels, trainingInstances, weights)

	with open('testlabels', 'r') as labels:
		testLabels = [int(x.strip('\r\n')) for x in labels.readlines()]

	with open('testimages', 'r') as testImages:
		img = [x.strip('\r\n') for x in testImages.readlines()]
		for i in range(len(img)):
			if i % 28 == 0:
				imageInstance = []
				for j in range(28):
					for k in range(28):
						if img[i+j][k] == "+" or img[i+j][k] == "#":
							imageInstance.append(1)
						else:
							imageInstance.append(0)
				testInstances.append(imageInstance)

	postTest = testing(weights, testInstances, testLabels)
	confusionMatr = confusionMatrix(postTest, testLabels)

	for line in confusionMatr:
		print(line)

def perceptron(trainingLabels, trainingInstances, weights):
	# subject to change
	for epoch in range(50):
		alpha = float(1)/float(1 + epoch)  
		for i in range(len(trainingLabels)):

			classifier = []
			for j in range(10):
				classifier.append(dotProduct(weights[j], trainingInstances[i]))

			c = -1
			max = -1
			for j in range(10):
				if classifier[j] > max:
					c = j
					max = classifier[j]

			if c != trainingLabels[i]:
				weights[c] = vectorSubtraction(weights[c], scalarProduct(alpha, trainingInstances[i]))
				weights[trainingLabels[i]] = vectorAddition(weights[trainingLabels[i]], scalarProduct(alpha, trainingInstances[i]))

		checkAccuracy(trainingLabels, trainingInstances, weights)

def testing(weights, testInstances, testLabels):
	postTest = []
	for i in range(len(testInstances)):
		d = []
		for j in range(10):
			d.append(dotProduct(weights[j], testInstances[i]))
		postTest.append(d)
	return postTest

def confusionMatrix(postTest, testLabels):
	confusionMatrix = []
	for i in range(10):
		confusionMatrix.append([])
		for j in range(10):
			confusionMatrix[i].append(0)

	numInstances = [0 for x in range(10)]
	for i in range(len(testLabels)):
		numInstances[testLabels[i]] = numInstances[testLabels[i]] + 1

	for i in range(len(postTest)):
		max = -100000000
		indexMax = -1
		for j in range(len(postTest[i])):
			if max < postTest[i][j]:
				max = postTest[i][j]
				indexMax = j

		confusionMatrix[testLabels[i]][indexMax] = confusionMatrix[testLabels[i]][indexMax] + 1

	for i in range(10):
		for j in range(10):
			if numInstances[i] != 0:
				confusionMatrix[i][j] = float(confusionMatrix[i][j])/float(numInstances[i])

	return confusionMatrix

def checkAccuracy(trainingLabels, trainingInstances, weights):
	postTest = testing(weights, trainingInstances, trainingLabels)
	confusionMatr = confusionMatrix(postTest, trainingLabels)
	sum = 0
	for i in range(10):
		sum = sum + confusionMatr[i][i]

	print(sum/10)

main()
