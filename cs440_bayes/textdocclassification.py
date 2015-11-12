from math import log
import re

def multinomial_bayes(training_file):
	"""
	Multionomial naive bayes classification

	Takes a file as an argument, parses the input data, and returns a dictionary of dictionaries, with the key being a word, 
	and the value being a dictionary of classes, with the values being the probabilities of being that class.
	Also returns the priors for each class
	Also returns a dictionary of likelihoods divided by words
	"""
	training_values = {}
	all_likelihoods = {}
	all_words = {}
	words_count = {}
	priors = {}
	total_docs = 0
	with open(training_file, 'r') as training_set:			#Open the training set
		for line in training_set:
			total_docs += 1
			class_type = line[0:2].strip()
			if class_type not in training_values:
				training_values[class_type] = {}
			if class_type not in priors:
				priors[class_type] = 1
			else:
				priors[class_type] += 1
			line = line.replace(class_type, "", 1).strip()
			wordlist = line.split(" ")
			for word in wordlist:
				wordcount = word.split(":")
				if wordcount[0] not in training_values[class_type]:			#Add the word and the count to the appiopriate classes dictionary
					training_values[class_type][wordcount[0]] = int(wordcount[1])
				else:
					training_values[class_type][wordcount[0]] += int(wordcount[1])
				if class_type not in words_count:
					words_count[class_type] = int(wordcount[1])
				else:
					words_count[class_type] += int(wordcount[1])
				all_words[wordcount[0]] = {} 			#Insert the word into the dictionary

	words_len = len(all_words.keys())
	for word in all_words.keys():
		likelihoods = {}
		for class_type, words in training_values.iteritems():
			if class_type not in all_likelihoods:
				all_likelihoods[class_type] = {}
			if word in words:
				likelihoods[class_type] = float(words[word] + 1)/(words_count[class_type] + words_len)			#Find  P(word | class) = (# of occurrences of this word in docs from this class + 1)/ (total # of words in docs from this class + V)
				all_likelihoods[class_type][word] = likelihoods[class_type]
			else:
				likelihoods[class_type] = 1.0/(words_count[class_type] + words_len)
		all_words[word] = likelihoods			#The likelihhods for each class are a dictionary of probabilities for both classes
	for class_type in priors.keys():
		priors[class_type] = float(priors[class_type])/total_docs			#Calculate the priors for each class

	return all_words, priors, all_likelihoods


def bernoulli_bayes(training_file):
	"""
	Bernoulli naive bayes classification

	Takes a file as an argument, parses the input data, and returns a dictionary of dictionaries, with the key being a word, 
	and the value being a dictionary of classes, with the values being the probabilities of being that class.
	Also returns the priors for each class
	Also returns a dictionary of likelihoods divided by words
	"""
	training_values = {}
	all_likelihoods = {}
	all_words = {}
	docs_count = {}
	priors = {}
	total_docs = 0
	with open(training_file, 'r') as training_set:			#Open the training set
		for line in training_set:
			total_docs += 1
			class_type = line[0:2].strip()
			if class_type not in training_values:
				training_values[class_type] = {}
			if class_type not in priors:
				priors[class_type] = 1
			else:
				priors[class_type] += 1
			if class_type not in docs_count:
				docs_count[class_type] = 1
			else:
				docs_count[class_type] += 1
			line = line.replace(class_type, "", 1).strip()
			wordlist = line.split(" ")
			for word in wordlist:
				wordcount = word.split(":")
				if wordcount[0] not in training_values[class_type]:			#Add the word and the count to the appiopriate classes dictionary
					training_values[class_type][wordcount[0]] = 1
				else:
					training_values[class_type][wordcount[0]] += 1
				all_words[wordcount[0]] = {} 			#Insert the word into the dictionary

	words_len = len(all_words.keys())
	for word in all_words.keys():
		likelihoods = {}
		for class_type, words in training_values.iteritems():
			if class_type not in all_likelihoods:
				all_likelihoods[class_type] = {}
			if word in words:
				likelihoods[class_type] = float(words[word] + 1)/(docs_count[class_type] + total_docs)			#Find  P(word | class) = (# of occurrences of this word in docs from this class + 1)/ (total # of words in docs from this class + V)
				all_likelihoods[class_type][word] = likelihoods[class_type]
			else:
				likelihoods[class_type] = 1.0/(docs_count[class_type] + total_docs)
		all_words[word] = likelihoods			#The likelihhods for each class are a dictionary of probabilities for both classes
	for class_type in priors.keys():
		priors[class_type] = float(priors[class_type])/total_docs			#Calculate the priors for each class

	return all_words, priors, all_likelihoods


def runner(bayes_function, train_file, testing_file, classes):
	"""
	The main function runs the classifier using the given bayes function and given train and testing files, and then it classifies the testing set 
	"""
	words, priors, all_likelihoods = bayes_function(train_file)		#Run the training portion of the classifier
	success = {}
	total = {}
	classification = {}
	for item in classes:				#Generate the classification matrix:
		classification[item] = {}
		for item2 in classes:
			classification[item][item2] = 0
	total_success = 0
	total_test = 0
	with open(testing_file) as test_file:		#Open the testing set
	 	for line in test_file:
	 		total_test += 1
	 		class_type = line[0:2].strip()
		 	if class_type not in total:					#Add one to the count for this class
				total[class_type] = 1
			else:
				total[class_type] += 1
			total_likelihoods = {}
			line = line.replace(class_type, "", 1).strip()
			wordlist = line.split(" ")
			for class_t in priors.keys():					#Go through all the classes for each word in the document
				total_likelihoods[class_t] = log(priors[class_t])		#Take the log of the prior
				for word in wordlist:
					wordcount = word.split(":")
					if wordcount[0] in words:
						for i in range(int(wordcount[1])):
							total_likelihoods[class_t] += log(words[wordcount[0]][class_t])			#Calculate the log of the liklihood for each word in the document
			best = sorted(total_likelihoods.items(), key=lambda x:x[1])
			res = best[len(best) - 1]								#Take the class with the lowest likelihood
			if res[0] == class_type:
				total_success += 1
				if res[0] not in success:
					success[res[0]] = 1
				else:
					success[res[0]] += 1
			classification[class_type][res[0]] += 1
	print("Total Success Ratio: %f" % (float(total_success)/float(total_test)))
	for key, value in success.iteritems():
		print("Success Ratio for %s: %f" % (key, (float(value)/float(total[key]))))
	for key, value in classification.iteritems():
		count = 0
		for class_t, number in value.iteritems():
			count += number
		for class_t, number in value.iteritems():
			value[class_t] = float(number)/float(count)
	print("Confusion Matrix:")
	print("	" + "		".join(classes))
	for item in classes:
		values = [classification[item][item2] for item2 in classes]
		print(item + "	" + "	".join(["{0:.2f}".format(item2) for item2 in values]))
	print("")
	for item in classes:
		print("Top 20 words with greatest likelihoods for class %s" % item)
		best = sorted(all_likelihoods[item].items(), key=lambda x:x[1], reverse=True)
		for item2 in best[:20]:
			print("%s - %f" % (item2[0], item2[1]))
		print("")

def main():
	print("Running Multinomial Bayes for Spam Detection")
	runner(multinomial_bayes, "spam_detection/train_email.txt", "spam_detection/test_email.txt", ['0','1'])
	print("")
	print("Running Bernoulli Bayes for Spam Detection")
	runner(bernoulli_bayes, "spam_detection/train_email.txt", "spam_detection/test_email.txt", ['0','1'])
	print("")
	print("Running Multinomial Bayes for Movie Reviews")
	runner(multinomial_bayes, "sentiment/rt-train.txt", "sentiment/rt-test.txt", ['-1', '1'])
	print("")
	print("Running Bernoulli Bayes for Movie Reviews")
	runner(bernoulli_bayes, "sentiment/rt-train.txt", "sentiment/rt-test.txt", ['-1', '1'])
	print("")
	print("Extra Credit Portion for 2.2:")
	print("Running Multinomial Bayes for 8 Category")
	runner(multinomial_bayes, "8category/8category.training.txt", "8category/8category.testing.txt", ['0', '1', '2', '3', '4', '5', '6', '7'])
	print("")
	print("Running Bernoulli Bayes for 8 category")
	runner(bernoulli_bayes, "8category/8category.training.txt", "8category/8category.testing.txt", ['0', '1', '2', '3', '4', '5', '6', '7'])


if __name__ == "__main__":
	main()