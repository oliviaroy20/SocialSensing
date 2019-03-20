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

def choose_test(train_data, train_truth):
	test_data = list()
	test_truth= list()
	for idx in range(200):
		rand = random.randint(0, len(train_data)-1)
		test_data.append(train_data[rand])
		test_truth.append(train_truth[rand])
		train_data.pop(rand)
		train_truth.pop(rand)
	return train_data, train_truth, test_data, test_truth


if __name__ == '__main__':
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

	print("svm: {}".format(correct[True]/sum(correct)))
