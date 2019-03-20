##### This is a first attempt to classify the tweets ######
import csv
from textblob import TextBlob
import numpy as np
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
split = int(2*len(text)/3)

text_train = text[:split]
text_test = text[split:]
classify_train = classify[:split]
classify_test = classify[split:]
sentiment_train = sentiment[:split]
sentiment_test = sentiment[split:]

# Gives accuracy for sentiment
correct = [0,0]
for sent, c in zip(sentiment, classify):
    if c == -1:
        correct[sent<-0.1] += 1
    elif c == 0:
        correct[sent>=-0.1  and sent<=0.1] += 1
    else:
        correct[sent>0.1] += 1
print("Sentiment accuracy: {}".format(correct[True]/sum(correct)))

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(text_train)
#X_train_counts.shape
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

X_new_counts = count_vect.transform(text_test)
X_new_tfidf = tf_transformer.transform(X_new_counts)

from sklearn.naive_bayes import MultinomialNB, BernoulliNB, ComplementNB

# Goes through different classifiers and fits/predicts with them
models = ["MultinomialNB", "BernoulliNB", "ComplementNB"]
for i, classifier in enumerate((MultinomialNB(), BernoulliNB(), ComplementNB())):
    clf = classifier.fit(X_train_tf, classify_train)
    #clf = classifier.fit(features, classify_train)
    
    predicted = clf.predict(X_new_tfidf)
    #predicted = clf.predict(features_test)

    correct = [0,0]
    for doc, category in zip(classify_test, predicted):
        correct[str(doc)==str(category)] += 1

    print("{}: {}".format(models[i],correct[True]/sum(correct)))
