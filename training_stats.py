with open("NewClassifyObamacare.csv", "r") as f:
	pos = 0
	neg = 0
	neutral = 0
	for line in f.readlines():
		line = line.strip().split(';')
		if line[-1] == '1':
			pos +=1
		if line[-1] == '-1':
			neg +=1
		if line[-1] == '0':
			neutral += 1
	print("positive: {}".format(pos))
	print("negative: {}".format(neg))
	print("neutral: {}".format(neutral))
