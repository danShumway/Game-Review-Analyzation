import nltk
wordReviewNet = {}


class Model:

	def __init__(self):
		self.wordReviewNet = {}
		self.exclude = None #define a function here that disqualifies words?
		self.baselines = []

	def UpdateBaselines(self, train_reviews):
		self.scoreBaselines = []
		self.trainingSize = len(train_reviews)

		num = 0
		total = 0
		#
		self.modes = {}
		self.baselines = []
		#
		import math
		for review in train_reviews:
			#For average
			total += int(review['score'])
			num += 1
			#For baselines
			if(review['score'] not in self.mode): self.mode[review['score']] = 0
			self.mode[review['score']] += 1

		self.mode = 0 #Assumes 1 mode.
		mean_index = total/2 #Assumes 1 median.  Eh, I'm just not going to calculate this right now.
		
		for score in range(0,11):
			if(self.modes[self.mode] < self.modes[score]):
				self.mode = score

			self.baselines.append(float(self.mode[str(score)])/num)

		self.mean = float(total)/num #Average.


		#varience = 0
		#dev = math.sqrt(varience/total)


	#If self.exclude is not defined, should still run.
	def UpdateWordNet(review, score):
		tokens = nltk.word_tokenize(review)
		for word in tokens:
			if(word not in wordReviewNet):
				if(self.exclude == None or self.exclude(word)):
					wordReviewNet[word] = []
					for i in range(0, 12):
						wordReviewNet[word].append(0)
				wordReviewNet[word][score]+=1
				wordReviewNet[word][11]+=1 #Count of how often we've seen the word.

	#
	def Train(train_data):
		for review in train_data:
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
					model[i] += float(self.wordReviewNet[word][i])/self.wordReviewNet[word][11] - modePercentage[i]

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