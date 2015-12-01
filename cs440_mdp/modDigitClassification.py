import sys
import copy
import math

def main():
	trainingLabels = []
	trainingImages = []

	with open('traininglabels', 'r') as labels:
		trainingLabels = [int(x.strip('\r\n')) for x in labels.readlines()]

	with open('trainingimages', 'r') as images:
		img = [x.strip('\r\n') for x in images.readlines()]
		for i in range(len(img)):
			if i % 28 == 0:
				imageInstance = []
				for j in range(28):
					imageInstance.append([])
					for k in range(28):
						imageInstance[j].append(img[i + j][k])
				trainingImages.append(imageInstance)

	perceptron(trainingLabels, trainingImages)

def perceptron(trainingLabels, trainingImages):
	

main()
