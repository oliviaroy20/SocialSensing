##### This is a first attempt to classify the tweets ######
import csv
from textblob import TextBlob
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, ComplementNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC



def getsplits(data): #everything starts in test and moves into the training sets
    train_data = list()
    train_class = list()
    test_data = list()
    test_class = list()
    looked = list()
    switched = 5
    dems = 10
    repub = 10
    total = 0
    while total < len(data):
        rand = random.randint(0, len(data)-1)
        curr = data[rand]
        if rand in looked:
            continue
        elif curr[0] == 'R' and curr[-1] == 0 and switched > 0:
            train_data.append(curr[:-1])
            train_class.append(curr[-1])
            switched -= 1
            looked.append(rand)
        elif curr[0] == 'D' and dems > 0:
            train_data.append(curr[:-1])
            train_class.append(curr[-1])
            looked.append(rand)
            dems -= 1
        elif curr[0] == 'R' and repub > 0:
            train_data.append(curr[:-1])
            train_class.append(curr[-1])
            looked.append(rand)
            repub -= 1
        else:
            test_data.append(curr[:-1])
            test_class.append(curr[-1])
            looked.append(rand)
    return train_data, train_class, test_data, test_class

iterations = 20
models = ["MultinomialNB", "BernoulliNB", "LinearSVC", "ComplementNB", "MLPClassifier"]
for i in range(iterations):
    # Open supervised classification file
    with open('PredictorData.csv','r') as f:
        csv_reader = csv.reader(f, delimiter=",")
        data = []
        for row in csv_reader:
            density = row[6]/row[3]
            compiled = []
            for i, d in row:
                if i == 0 or i==3 or i==6 or i == 2:
                    continue
                else:
                    compiled.append(d)
            compiled.append(density)
            compiled.append(row[2])
            data.append(compiled)


    train_data, train_class, test_data, test_class = get_splits(data)


    # Goes through different classifiers and fits/predicts with them
    for j, classifier in enumerate((MultinomialNB(), BernoulliNB(), LinearSVC(), ComplementNB(), MLPClassifier())):
        clf = classifier.fit(train_data, train_class)

        predicted = clf.predict(test_data)

        correct = [0,0]
        for doc, category in zip(test_class, predicted):
            correct[str(doc)==str(category)] += 1
            try:
                avg_predict[j][int(category)+1] += 1
            except:
                continue

        #print("{}: {}".format(models[i],correct[True]/sum(correct)))
        percent = correct[True]/ sum(correct)

        # print("svm: {}".format(correct[True]/sum(correct)))
        avg[j] += percent

for i,model in enuerate(models):
    print(model + ": {}".format(avg[i]/iterations))
    print("Anti: {}, Neutral: {}, Pro: {}".format(avg_predict[i][0]/sum(avg_predict[i]), avg_predict[i][1]/sum(avg_predict[i]), avg_predict[i][2]/sum(avg_predict[i])))
'''
print("avgMNB: {}".format(avg[0]/iterations))
print("Anti: {}, Neutral: {}, Pro: {}".format(avg_predict[0][0]/sum(avg_predict[0]),avg_predict[0][1]/sum(avg_predict[0]),avg_predict[0][2]/sum(avg_predict[0])))
print("avgBNB: {}".format(avg[1]/iterations))
print("Anti: {}, Neutral: {}, Pro: {}".format(avg_predict[1][0]/sum(avg_predict[1]),avg_predict[1][1]/sum(avg_predict[1]),avg_predict[1][2]/sum(avg_predict[1])))
print("avgSVM: {}".format(avg[2]/iterations))
print("Anti: {}, Neutral: {}, Pro: {}".format(avg_predict[2][0]/sum(avg_predict[2]),avg_predict[2][1]/sum(avg_predict[2]),avg_predict[2][2]/sum(avg_predict[2])))
print("avgCNB: {}".format(avg[3]/iterations))
print("Anti: {}, Neutral: {}, Pro: {}".format(avg_predict[3][0]/sum(avg_predict[3]),avg_predict[3][1]/sum(avg_predict[3]),avg_predict[3][2]/sum(avg_predict[3])))
print("avgMLP: {}".format(avg[4]/iterations))
print("Anti: {}, Neutral: {}, Pro: {}".format(avg_predict[3][0]/sum(avg_predict[4]),avg_predict[4][1]/sum(avg_predict[3]),avg_predict[4][2]/sum(avg_predict[4])))
print("sent avg: {}".format(sent_avg/iterations))
print(sent_avg_p)
print("Anti: {}, Neutral: {}, Pro: {}".format(sent_avg_p[0]/sum(sent_avg_p),sent_avg_p[1]/sum(sent_avg_p), sent_avg_p[2]/sum(sent_avg_p)))
'''
