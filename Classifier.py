##### This is a first attempt to classify the tweets ######
import csv
from textblob import TextBlob
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC
#could not import ComplementNB


def getsplits(text, classify, sentiment): #everything starts in test and moves into the training sets
	text_train= list()
	classify_train = list()
	sentiment_train = list()
	pos = 170
	neg = 170
	neutral = 60
	while (pos >0 or neg >0 or neutral>0):
		rand = random.randint(0, len(text)-1)
		truth = classify[rand]
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
			text_train.append(text[rand])
			classify_train.append(truth)
			sentiment_train.append(sentiment[rand])
			text.pop(rand)
			classify.pop(rand)
			sentiment.pop(rand)
	return text_train, text, classify_train, classify, sentiment_train, sentiment

avg = [0, 0, 0]
sent_avg = 0
for i in range(100):
	text = []
	sentiment = []
	classify = []
	features = []
	# Open supervised classification file
	with open('NewClassifyObamacare.csv','r') as f:
		csv_reader = csv.reader(f, delimiter=";")
		for row in csv_reader:
		    text.append(row[4])
		    blob = TextBlob(row[4])
		    sentiment.append(blob.sentiment.polarity)
		    classify.append(row[10])

	# Find where to split the testing and training
	# split = int(2*len(text)/3)
	#
	# text_train = text[:split]
	# text_test = text[split:]
	# classify_train = classify[:split]
	# classify_test = classify[split:]
	# sentiment_train = sentiment[:split]
	# sentiment_test = sentiment[split:]

	text_train, text_test, classify_train, classify_test, sentiment_train, sentiment_test = getsplits(text, classify, sentiment)
	# Gives accuracy for sentiment

	correct = [0,0]
	for sent, c in zip(sentiment, classify):
		if c == -1:
		    correct[sent<-0.1] += 1
		elif c == 0:
		    correct[sent>=-0.1  and sent<=0.1] += 1
		else:
		    correct[sent>0.1] += 1
	# print("Sentiment accuracy: {}".format(correct[True]/sum(correct)))
	sent_avg += correct[True]/sum(correct)

	count_vect = CountVectorizer()

	X_train_counts = count_vect.fit_transform(text_train)
	#X_train_counts.shape
	# use_idf=False
	tf_transformer = TfidfTransformer().fit(X_train_counts)
	X_train_tf = tf_transformer.transform(X_train_counts)

	X_new_counts = count_vect.transform(text_test)
	X_new_tfidf = tf_transformer.transform(X_new_counts)



	# Goes through different classifiers and fits/predicts with them
	models = ["MultinomialNB", "BernoulliNB", "LinearSVC", "ComplementNB"]
	for i, classifier in enumerate((MultinomialNB(), BernoulliNB(), LinearSVC())):
		clf = classifier.fit(X_train_tf, classify_train)
	#clf = classifier.fit(features, classify_train)

		predicted = clf.predict(X_new_tfidf)
		#predicted = clf.predict(features_test)

		correct = [0,0]
		for doc, category in zip(classify_test, predicted):
		    correct[str(doc)==str(category)] += 1

	# print("{}: {}".format(models[i],correct[True]/sum(correct)))
		percent = correct[True]/ sum(correct)
	# print("svm: {}".format(correct[True]/sum(correct)))
		avg[i] += percent
print("avgMNB: {}".format(avg[0]/100))
print("avgBNB: {}".format(avg[1]/100))
print("avgSVM: {}".format(avg[2]/100))
print("sent avg: {}".format(sent_avg/100))
