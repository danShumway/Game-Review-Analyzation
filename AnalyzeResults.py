import json
f = open('databases/reviews.json', 'r')
reviewers = json.loads(f.read())

print "Analyzing results"

#----------------BASIC STATS------------------------------

print str(len(reviewers)) + " reviewers found."

duplicates = {}

for reviewer in reviewers:
	if(len(reviewers[reviewer]) > 4):
		duplicates[reviewer] = reviewers[reviewer]

print str(len(duplicates)) + " reviewers with more than 4 reviews"


print "\n"

#---------------------AVERAGES---------------------------

print "Let's start by just checking to see review averages."

total = 0
num = 0
for reviewer in reviewers:
	for review in reviewers[reviewer]:
		total += int(review['score'])
		num += 1

mean = float(total)/num
print "Mean: " + str(mean)
#print "Median: " + str()

varience = 0
mode = {} 
modePercentage = []
import math
for reviewer in reviewers:
	for review in reviewers[reviewer]:
		if(review['score'] not in mode): mode[review['score']] = 0
		mode[review['score']] += 1
		varience += math.pow(float(review['score']) - mean, 2)

dev = math.sqrt(varience/total)
print "Standard Deviation: " + str(dev)

for score in range(0,11):
	print(str(score) + " stars: " + str(mode[str(score)]) + ", " + str(int(float(mode[str(score)])/num*100)))

#Actually important.
for score in range(0,11):
	modePercentage.append(float(mode[str(score)])/num)


print '\n'

print('defining functions')

import nltk
wordReviewNet = {}
def UpdateWordNet(review, score):
	tokens = nltk.word_tokenize(review)
	for word in tokens:
		if(word not in wordReviewNet):
			wordReviewNet[word] = []
			for i in range(0,12):
				wordReviewNet[word].append(0)
		wordReviewNet[word][score]+=1;
		wordReviewNet[word][11]+=1;

def Train(reviewers):
	for reviewer in reviewers:
		for review in reviewers[reviewer]: 
			UpdateWordNet(review['review'], int(review['score']))

def Guess(review, score, show):
	if(show):
		print review.encode('utf-8') + '\n'
	tokens = nltk.word_tokenize(review)
	model = []
	for i in range(0,11):
		model.append(0)
	for word in tokens:
		if(word in wordReviewNet):
			for i in range(0,11):
				model[i] += float(wordReviewNet[word][i])/wordReviewNet[word][11] - modePercentage[i]

	maxNum = 0
	maxIndex = 0
	for i in range(0, 11):
		if(model[i] > maxNum):
			maxNum = model[i]
			maxIndex = i
		if(show):
			print str(i) + " likelyhood: " + str(model[i])
	if(show):
		print("Actual score: " + str(score) + ", guessed " + str(maxIndex))
		print '\n'

	return(int(score) == int(maxIndex))


print('training model')
Train(reviewers)
print('done\n')

import random
def DoGuess(show):
	key = random.choice(reviewers.keys())
	return Guess(reviewers[key][0]['review'], reviewers[key][0]['score'], show)

correct = 0
trials = 1000
#for i in range(0,trials):
#	if(DoGuess(False)):
#		correct+=1

#print "\n Accuracy :" + str(float(correct)/trials)

from Evaluation import evaluate_dist
evaluate_dist(reviewers, wordReviewNet, modePercentage)
