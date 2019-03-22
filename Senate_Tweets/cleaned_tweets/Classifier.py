##### This is a first attempt to classify the tweets ######
import csv
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import ComplementNB
import os
from langdetect import detect
#could not import ComplementNB

text = []
sentiment = []
classify_train = []
features = []
# Open supervised classification file
with open('../../NewClassifyObamacare.csv','r') as f:
    csv_reader = csv.reader(f, delimiter=";")
    for row in csv_reader:
        text.append(row[4])
        classify_train.append(row[10])

#text_train, text_test, classify_train, classify_test, sentiment_train, sentiment_test = getsplits(text, classify, sentiment)
# Gives accuracy for sentiment

correct = [0,0]

count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(text)
#X_train_counts.shape
# use_idf=False
tf_transformer = TfidfTransformer().fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

for filename in os.listdir("."):
    if ".csv" not in filename:
        continue
    text_test = []
    with open(filename,'r') as f:
        csv_reader = csv.reader(f, delimiter=";")
        for row in csv_reader:
            try:
                d = detect(row[4])

                if d == "en":
                    text_test.append(row[4])
            except:
                continue
    
    X_new_counts = count_vect.transform(text_test)
    X_new_tfidf = tf_transformer.transform(X_new_counts)



    # Goes through different classifiers and fits/predicts with them
    classifier = ComplementNB()
    clf = classifier.fit(X_train_tf, classify_train)
    #clf = classifier.fit(features, classify_train)

    predicted = clf.predict(X_new_tfidf)
	#predicted = clf.predict(features_test)

    classification = [0,0,0]
    errors = 0

    for predict in predicted:
        try:
            classification[int(predict)+1] += 1
        except:
            errors += 1

# print("{}: {}".format(models[i],correct[True]/sum(correct)))
    print(filename)
    print("Pro-Obamacare: {} --- {}%".format(classification[2],round(classification[2]/sum(classification),4)*100))
    print("Neutral: {} --- {}%".format(classification[1],round(classification[1]/sum(classification),4)*100))
    print("Anti-Obamacare: {} --- {}%".format(classification[0],round(classification[0]/sum(classification),4)*100))
    print("Errors: {}".format(errors))
    print("")
# print("svm: {}".format(correct[True]/sum(correct)))
