Game-Review-Analyzation
=======================

Experiments with doing sentiment analysis on game reviews to predict scores and form maps of individual preferences.

##How does it work?

The model loops through a training set of reviews and builds a dictionary of all the found words, matching them up with the number of occurances correlated with each review score (0-10).  It then loops through reviews from a test set and tallies up a makeshift likelyhood for each possible review score from each word found in the review.

##How do I use it?

The model is split into 3 different scripts.

 - **getGames.py**:
 - **getReviews.py**:
 - **AnalyzeResults.py**:

Normally, you would be required to run these scripts in order, as each relies on the output from the previous script.  However, because we have included the output from each script when we last ran them, you'll likely want to run only AnalyzeResults.py.

Running this script will output some data about the training set, train the model (storing the dictionary in databases/wordNet.json, and then test the model, outputing an example, and the weighted accuracy from the test.
