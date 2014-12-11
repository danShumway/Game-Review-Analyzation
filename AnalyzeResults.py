import json
import random


f = open('databases/reviewsAll.json', 'r')
reviewers = json.loads(f.read())

print "Analyzing results"

#----------------BASIC STATS------------------------------

duplicates = {}

train_size = 22000
train_reviews = []
test_reviews = []

total_set = []
for reviewer in reviewers:
	for review in reviewers[reviewer]:
		total_set.append(review)
random.shuffle(total_set)

c = train_size
for review in total_set:
	if(c > 0):
		train_reviews.append(review)
		c-=1
	else:
		test_reviews.append(review)

print str(len(test_reviews) + len(train_reviews)) + " reviews found."


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

from Model import Model

test_model = Model()

test_model.UpdateBaselines(train_reviews)

print "Mean: " + str(test_model.mean)


print('training model')

from nltk.corpus import stopwords
test_model.exclude = stopwords.words('english')
test_model.Train(train_reviews)
print('done, running evaluations.\n')


from Evaluation import evaluate_rigorous_dist
evaluate_rigorous_dist(test_reviews, test_model.wordReviewNet, modePercentage, test_model)

#test_model.Guess(test_reviews[0]["review"], test_reviews[0]["score"], True)

### Generate confusion matrix of scores
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

score_true = []
score_guess = []

for i, review in enumerate(test_reviews):
    score_true.append(int(review['score']))
    score_guess.append(test_model.GuessScore(review['review']))

cm = confusion_matrix(score_true, score_guess)
plt.matshow(cm)
plt.colorbar()
plt.xlabel('Predicted Score')
plt.ylabel('True Score')

### Precision Recall F1
from sklearn.metrics import precision_recall_fscore_support

prfs = precision_recall_fscore_support(score_true, score_guess)

