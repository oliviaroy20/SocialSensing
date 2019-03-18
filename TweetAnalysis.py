from textblob import TextBlob
import csv
import json

def assign_value(dictionary, polarity):
    if polarity > 0:
        dictionary["positive"] += 1
    else:
        dictionary["negative"] += 1

senators = []
names = []
politican_mentions = {}
with open('Senators.csv', 'r') as senatorsfile:
    senatorreader = csv.reader(senatorsfile, delimiter=';')
    for line in senatorreader:
        senators.append(line[2].strip())
        politican_mentions[line[2].strip()] = {"positive":0, "negative":0}

with open('Senators_twitter', 'r') as senatorsfile:
    for line in senatorsfile:
        senators.append(line.strip())
        politican_mentions[line.strip()] = {"positive":0, "negative":0}

with open('NewObamacare.csv', 'r') as csvfile:
    tweetreader = csv.reader(csvfile, delimiter=';')
    pos_neg = {"positive": 0, "negative":0}
    username = {}
    politican_username = {}
    for i, row in enumerate(tweetreader):
        if i == 0:
            continue
        blob = TextBlob(row[4])
        for politican in senators:
            if politican in row[4]:
                assign_value(politican_mentions[politican], blob.sentiment.polarity)
            if politican in row[4] and row[0] not in politican_username.keys():
                if blob.sentiment.polarity > 0:
                    politican_username[row[0]] = {"positive": 1, "negative": 0}
                else:
                    politican_username[row[0]] = {"positive": 0, "negative": 1}
            if politican in row[4]:
                assign_value(politican_username[row[0]], blob.sentiment.polarity)
        if row[0] not in username.keys():
            username[row[0]] = {"positive": 0, "negative": 0}
        assign_value(username[row[0]], blob.sentiment.polarity)
        assign_value(pos_neg, blob.sentiment.polarity)
    positive = 0
    negative = 0
    for user, opinion in username.items():
        if opinion["positive"] > opinion["negative"]:
            positive += 1
        else:
            negative += 1
    print("Positive: " + str(positive) + "\tNegative: " + str(negative))
    positive = 0
    negative = 0
    for user, opinion in politican_username.items():
        if opinion["positive"] > opinion["negative"]:
            positive += 1
        else:
            negative += 1
    print("Politician analysis: Positive: " + str(positive) + "\tNegative: " + str(negative))

real_politican = {}
for politican, opinion in politican_mentions.items():
    if opinion["positive"] != 0 or opinion["negative"] != 0:
        real_politican[politican] = opinion

party = {"R":{"positive":0, "negative":0},"D":{"positive":0,"negative":0},"I":{"positive":0,"negative":0}}
voted = {"Yea":{"positive":0, "negative":0}, "Nay":{"positive":0,"negative":0}}
with open('RepealHealthCareAct.json','r') as votinginfo:
    json_info = json.load(votinginfo)
    members = json_info["members"]
    for politican, opinion in real_politican.items():
        for member in members:
            if member["last_name"] in politican:
                print("Positive: " + str(opinion["positive"]) + "\tNegative: " + str(opinion["negative"]) + " \tVoted: " + member["vote_cast"] + "\tis " + member["party"])
                
                party[member["party"]]["negative"] += opinion["negative"]
                party[member["party"]]["positive"] += opinion["positive"]
                voted[member["vote_cast"]]["positive"] += opinion["positive"]
                voted[member["vote_cast"]]["negative"] += opinion["negative"]
            
print(party)
for key, value in party.items():
    print(key + " had ratio " + str(float(value["negative"]/(value["positive"] +value["negative"]))))
print(voted)
for key, value in voted.items():
    print(key + " had ratio " + str(float(value["negative"]/(value["negative"]+value["positive"]))))
