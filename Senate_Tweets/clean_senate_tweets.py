

if __name__ == '__main__':
	files = ['JerryMoran.csv', 'LindseyGraham.csv', 'LisaMurkowski.csv', 'RandPaul.csv', 'SenatorCollins.csv', 'SenBobCorker.csv', 'SenDeanHeller.csv', 'SenMikeLee.csv', 'TomCotton.csv']
	for file in files:
		with open(file, 'r') as f:
			file_write = open(file[:-4]+"_cleaned.csv", 'w')
			lines = f.readlines()
			for line in lines:
				if ("Obama" or "health") and "care" in line:
					file_write.write(line)
