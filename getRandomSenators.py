import json
import random

with open('RepealHealthCareAct.json', 'r') as f:
    data = json.load(f)

senators = data['members']
democrats = []
republicans = []
for s in senators:
    if s['party'] == 'R' and s['vote_cast'] == 'Yea':
        republicans.append(s["first_name"] + " " + s["last_name"])
    elif s['party'] == 'D' and s['vote_cast'] == 'Nay':
        democrats.append(s["first_name"] + " " + s["last_name"])

with open('SamplingSenators.txt', 'w') as f:
    randR = random.sample(republicans, 5)
    randD = random.sample(democrats, 5)

    for r in randR:
        f.write(r + "\n")
    for d in randD:
        f.write(d + "\n")

