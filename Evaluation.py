# Evaluate results by binning
def bin_results(review, actual, guess):
    # BINS:
    # 0 1 2
    # 3 4 5
    # 6 7 8 
    # 9 10 

    # Correct answer - don't bin
    if actual == guess:
        return True
    # Bin 1
    elif actual <= 2:
        if guess <=2:
            return True
        else:
            return False
    # Bin 2
    elif actual >= 3 & actual <= 5:
        if guess >= 3 & guess <= 5:
            return True
        else:
            return False
    # Bin 3
    elif actual >= 6 & actual <= 8:
        if guess >= 6 & guess <= 8:
            return True
        else:
            return False
    # Bin 4
    elif actual >= 9:
        if guess >= 9:
            return True
        else:
            return False
     

# Evaluate with partial credit accuracy
# (using inverse of distance from correct answer)
import random
import nltk
def evaluate_dist(reviewers, wRN, mP):
    correct = 0
    trials = 1000
    for i in range(0,trials):
    	correct += DoGuessDist(False, reviewers, wRN, mP)
     
    print "\n Weighted Accuracy :" + str(float(correct)/trials)

def evaluate_rigorous_dist(test_data, wRN, mP):
    correct = 0
    for review in test_data:
        correct += DoRigorousGuessDist(False, review, wRN, mP)

    print "\n Weighted Accuracy :" + str(float(correct)/len(test_data)) + " out of " + str(len(test_data)) + " trials."

def DoRigorousGuessDist(show, review, wRN, mP):
    return GuessDist(review['review'], review['score'], show, wRN, mP)


def DoGuessDist(show, reviewers, wRN, mP):
	key = random.choice(reviewers.keys())
	return GuessDist(reviewers[key][0]['review'], reviewers[key][0]['score'], show, wRN, mP)
            

#Some clarification.            
def GuessDist(review, score, show, wordReviewNet, modePercentage):
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
 
	# Return partial or full scores
	if int(score) == int(maxIndex):
		return 1
	elif abs(int(score) - int(maxIndex) ) > 3:
             return 0
	else:
		return 1 / float(abs(int(score) - int(maxIndex)))