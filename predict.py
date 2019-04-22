

def getData():
	file = open("name,pro,anti.csv", "r")
	data = list()
	for line in file:
		line = line.strip().split(',')
		dict ={"name": line[0], "party": line[1], "proObamacare":float(line[2]), "antiObamacare": float(line[3])}
		data.append(dict)
	return data



if __name__ == '__main__':
	data = getData()
	for senator in data:
		if senator["party"] == "R":
			if(senator["proObamacare"] > 55 ):
				print("Republican voting Nay")
				print(senator["name"])
		else: #democratic
			if(senator["antiObamacare"] > 85 ):
				print("Democrat voting Yay")
