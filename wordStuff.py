import json

f = open('databases/wordNet.json', 'r')
net = json.loads(f.read())


from nltk.corpus import stopwords

toSort = []
ignore = stopwords.words('english')
for word in net.keys():
	if word not in ignore:
		toSort.append([net[word][11], word])

toSort.sort(key=lambda s: s[0])

probabilities = []
for

print str(toSort[-1][1]) + ": " + str(net[toSort[-1][1]])

