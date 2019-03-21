from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
import random
import numpy as np
# from sklearn.model_selection import cross_val_score
# import pandas as pd
# from sklearn.naive_bayes import MultinomialNB

def readfile_train(filename):
	train_data = list()
	train_truth = list()
	file = open(filename, 'r')
	for line in file:
		line = line.strip().split(';')
		train_data.append(line[4].lower())
		train_truth.append(line[-1])
	return train_data, train_truth

def choose_test(test_data, test_truth):
	train_data = list()
	train_truth= list()
	pos = 170
	neg = 170
	neutral = 60
	while (pos >0 or neg >0 or neutral>0):
		rand = random.randint(0, len(test_data)-1)
		truth = test_truth[rand]
		add = False
		if truth == '1' and pos >0:
			pos -= 1
			add = True
		elif truth =='0' and neutral>0:
			neutral -=1
			add = True
		elif truth =='-1' and neg >0:
			neg -= 1
			add = True
		if add:
			train_data.append(test_data[rand])
			train_truth.append(truth)
			test_data.pop(rand)
			test_truth.pop(rand)

	# for idx in range(200):
	# 	rand = random.randint(0, len(train_data)-1)
	# 	test_data.append(train_data[rand])
	# 	test_truth.append(train_truth[rand])
	# 	train_data.pop(rand)
	# 	train_truth.pop(rand)
	return train_data, train_truth, test_data, test_truth


if __name__ == '__main__':
	avg = 0
	for i in range(100):
		train_data, train_truth = readfile_train('NewClassifyObamacare.csv')
		train_data, train_truth, test_data, test_truth = choose_test(train_data, train_truth)

		countVector = CountVectorizer()
		train_counts = countVector.fit_transform(train_data)
		transformer = TfidfTransformer().fit(train_counts)
		train_features = transformer.transform(train_counts)


		clf = LinearSVC()
		clf.fit(train_features, train_truth)

		test_counts = countVector.transform(test_data)
		transformer = TfidfTransformer().fit(test_counts)
		test_features = transformer.transform(test_counts)

		predicted = clf.predict(test_features)

		correct = [0,0]
		for doc, category in zip(test_truth, predicted):
			correct[str(doc)==str(category)] += 1
		percent = correct[True]/ sum(correct)
		# print("svm: {}".format(correct[True]/sum(correct)))
		avg += percent
	print("avg: {}".format(avg/100))
