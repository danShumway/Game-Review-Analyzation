import nltk
from nltk import RegexpTokenizer
import math
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
            if(review['score'] not in self.modes): self.modes[review['score']] = 0
            self.modes[review['score']] += 1

        self.mode = 0 #Assumes 1 mode.
        mean_index = total/2 #Assumes 1 median.  Eh, I'm just not going to calculate this right now.

        for score in range(0,11):
            if(self.modes[str(self.mode)] < self.modes[str(score)]):
                self.mode = score

            self.baselines.append(float(self.modes[str(score)])/num)

        self.mean = float(total)/num #Average.

        print self.baselines


        variance = 0
        for review in train_reviews:
            variance += math.pow(float(review['score']) - self.mean, 2)
            
        self.deviation = math.sqrt(variance/total)


    #If self.exclude is not defined, should still run.
    def UpdateWordNet(self, review, score):
        tokens = RegexpTokenizer(r'\w+').tokenize(review.lower())
        #tokens = nltk.word_tokenize(review)
        for word in tokens:
            if(word not in self.wordReviewNet):
                self.wordReviewNet[word] = []
                for i in range(0, 12):
                    self.wordReviewNet[word].append(0)
            self.wordReviewNet[word][score]+=1
            self.wordReviewNet[word][11]+=1 #Count of how often we've seen the word.

    #
    def Train(self, train_data):
        for review in train_data:
            self.UpdateWordNet(review['review'], int(review['score']))

        import json
        f = open('databases/wordNet.json', 'w')
        f.write(json.dumps(self.wordReviewNet))


    def Guess(self, review, score, show):
        if(show):
            print review.encode('utf-8') + '\n'
        tokens = RegexpTokenizer(r'\w+').tokenize(review.lower())
        #tokens = nltk.word_tokenize(review)
        model = []
        for i in range(0,11):
            model.append(0)
        for word in tokens:
            if(self.exclude == None or word not in self.exclude):#self.exclude(word)):
                if(word in self.wordReviewNet):
                    for i in range(0,11):
                        model[i] += ((float(self.wordReviewNet[word][i])/self.wordReviewNet[word][11]) - self.baselines[i])

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

       # return math.pow(int(score) - int(10), 2)
        return(int(score) == int(maxIndex))
        if (int(score) == int(maxIndex)):
            return 1
        elif (abs(int(score) - int(maxIndex) ) > 3):
            return 0
        else:
            return 1 / float(abs(int(score) - int(maxIndex)) + 1)
