import json
f = open('output.json', 'r')
reviewers = json.loads(f.read())

print "Analyzing results"

print str(len(reviewers)) + " reviewers found."

duplicates = {}

for reviewer in reviewers:
	if(len(reviewers[reviewer]) > 2):
		duplicates[reviewer] = reviewers[reviewer]

print str(len(duplicates)) + " reviewers with more than 2 reviews"
