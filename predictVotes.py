##### This is a first attempt to classify the tweets ######
import csv
from textblob import TextBlob
import numpy as np
import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, ComplementNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn import svm



def get_splits(data): #everything starts in test and moves into the training sets
    train_data = list()
    train_class = list()
    test_data = list()
    test_class = list()
    looked = list()
    switched = 3
    dems = 11
    repub = 11
    while len(looked) < len(data):
        rand = random.randint(0, len(data)-1)
        curr = data[rand]
        
        if rand in looked:
            continue
        elif len(train_data) < 25:
            train_data.append(curr[:-1])
            train_class.append(curr[-1])
            looked.append(rand)
        else:
            test_data.append(curr[:-1])
            test_class.append(curr[-1])
            looked.append(rand)
        '''
        if rand in looked:
            continue
        elif curr[0] == 1 and curr[-1] == 0 and switched > 0:
            train_data.append(curr[1:-1])
            train_class.append(curr[-1])
            switched -= 1
            looked.append(rand)
        elif curr[0] == 0 and dems > 0:
            train_data.append(curr[1:-1])
            train_class.append(curr[-1])
            looked.append(rand)
            dems -= 1
        elif curr[0] == 1 and repub > 0:
            train_data.append(curr[1:-1])
            train_class.append(curr[-1])
            looked.append(rand)
            repub -= 1
        else:
            test_data.append(curr[1:-1])
            test_class.append(curr[-1])
            looked.append(rand)
        '''
    return train_data, train_class, test_data, test_class

def findPerson(party, against, pro, ratio, data):
#def findPerson( against, pro, ratio, data):
    for row in data:
        #if row[1] == party and row[2] == against and row[3] == pro and row[4] == ratio:
        if row[2] == against and row[3] == pro and row[4] == ratio:
            return row[0]

def findVote(name, data):
    for row in data:
        if row[0] == name:
            return row[-1]
iterations = 200
models = ["MultinomialNB", "BernoulliNB", "LinearSVC", "ComplementNB", "MLPClassifier", "DecisionTree", "RandomForestClassifier", "ExtraTreesClassifier"]

data = []
names = []
vote_record = {}
with open('PredictorData.csv','r') as f:
    csv_reader = csv.reader(f, delimiter=",")
    for row in csv_reader:
        density = float(row[6])/float(row[3])
        compiled = []
        names_compiled = []
        for j, d in enumerate(row):
            if j == 0:
                names_compiled.append(d)
                vote_record[d] = []
            elif j==3 or j==6 or j == 2:
                continue
            elif j==1:
                if d == 'R':
                    compiled.append(1)
                    names_compiled.append(1)
                elif d == 'D':
                    compiled.append(0)
                    names_compiled.append(0)
                else:
                    compiled.append(2)
                    names_compiled.append(2)
            else:
                names_compiled.append(float(d))
                compiled.append(float(d))
        names_compiled.append(density)
        names_compiled.append(row[2])
        names.append(names_compiled)
        compiled.append(density)
        compiled.append(row[2])
        data.append(compiled)
col = ["party", "anti", "pro", "density"]
#col = [ "anti", "pro", "density"]
avg = []
guesses = []
for m in models:
    guesses.append([0,0])
    avg.append(0)
    for sen in vote_record.keys():
        vote_record[sen].append([0,0])
for i in range(iterations):
    # Open supervised classification file
    
    train_data, train_class, test_data, test_class = get_splits(data)
    train_data = pd.DataFrame(np.array(train_data), columns=col)
    train_class = pd.DataFrame(np.array(train_class))
    test_data_array = list(test_data)
    test_data = pd.DataFrame(np.array(test_data), columns = col)
    # Goes through different classifiers and fits/predicts with them
    for j, classifier in enumerate((MultinomialNB(), BernoulliNB(), LinearSVC(), ComplementNB(), MLPClassifier(), DecisionTreeClassifier(), RandomForestClassifier(), ExtraTreesClassifier())):
        clf = classifier.fit(train_data, train_class)
        predicted = clf.predict(test_data)
        correct = [0,0]
        for index, row in enumerate(test_data_array):
            sen = findPerson(row[0], row[1], row[2],row[3], names)
            #sen = findPerson(row[0], row[1], row[2],names)
            vote_record[sen][j][int(predicted[index])] += 1
        for doc, category in zip(test_class, predicted):
            correct[str(doc)==str(category)] += 1
            guesses[j][int(category)] += 1
        percent = float(correct[True])/ float(sum(correct))

        avg[j] += percent
for i,model in enumerate(models):
    print(model + ": {}".format(avg[i]/iterations))
    #print(str(int(round(100*guesses[i][1]/sum(guesses[i]),0))) + " yeas and " + str(int(round(100*guesses[i][0]/sum(guesses[i]),0))) + " nays")

    voted = [0,0]
    not_predicted = []
    for sen in vote_record.keys():
        vote = "nay"
        vote_num = 0
        if vote_record[sen][i][0] < vote_record[sen][i][1]:
            vote = "yea"
            vote_num = 1
            voted[1] += 1
        else:
            voted[0] += 1
        actualVote = findVote(sen,names)
        if vote_num != int(actualVote):
            not_predicted.append(sen)
    print(str(voted[1]) + " yeas and " + str(voted[0]) + " nays")
    print(not_predicted)

record = [0,0]
right = 0
wrong_people = []
for sen in vote_record.keys():
    vote = 0
    for i, model in enumerate(models):
        vote -= vote_record[sen][i][0] * float(avg[i]/iterations)**2
        vote += vote_record[sen][i][1] * float(avg[i]/iterations)**2
        '''
        if vote_record[sen][i][0] > vote_record[sen][i][1]:
            vote -= float(avg[i]/iterations)**3
        else:
            vote += float(avg[i]/iterations)**3
        '''
    actualVote = int(findVote(sen, names))
    if vote > 0:
        if actualVote == 1:
            right += 1
        else:
            wrong_people.append(sen)
            #print(sen)
        record[1] += 1
    else:
        if actualVote == 0:
            right += 1
        else:
            wrong_people.append(sen)
            #print(sen)
        record[0] += 1
print("Custom Ensemble: " + str(right/len(vote_record.keys())))
print(str(record[1]) + " yeas " + str(record[0]) + " nays")
print(wrong_people)
