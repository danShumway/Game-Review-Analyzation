Game-Review-Analyzation
=======================

Experiments with doing sentiment analysis on game reviews to predict scores and form maps of individual preferences.

##How does it work?

The model loops through a training set of reviews and builds a dictionary of all the found words, matching them up with the number of occurances correlated with each review score (0-10).  It then loops through reviews from a test set and tallies up a makeshift likelyhood for each possible review score from each word found in the review.

##How do I use it?

Good question, I'll get back to you once the code is cleaned up.
