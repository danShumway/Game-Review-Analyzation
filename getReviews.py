#Read in reviews from API.

# How do we use sentiment analysis?  (Determine the subject(predicate) for each sentence.)  (Determine sentiment for that subject.)  - Figure out how connected certain words are.

import unirest

unirest.timeout(45);

url = "https://byroredux-metacritic.p.mashape.com/user-reviews?page_count=5&url=http%3A%2F%2Fwww.metacritic.com%2Fgame%2F"
url2 = "https://byroredux-metacritic.p.mashape.com/user-reviews?page_count=5&url=";
games_to_test = []#['Minecraft', 'World of Warcraft', 'Diablo III', 'Half-Life 2', 'Starcraft', 'The Sims 3', 'Guild Wars', 'Myst', 'Riven', 'Far Cry', 'The Witcher', 'Spore', 'Quake', 'American McGee\'s Alice', 'Dungeon Siege', 'Duke Nukem', 'BioShock', 'Frogger', 'Hotel Giant']


reviewers = {}
games = {}

def loadGames(file):
	import json
	f = open(file, 'r')
	temp = json.loads(f.read())
	for g in temp:
		games_to_test.append(g[0])


#New import
def addReviewersNonSelective(game, game_url, name):
	response = unirest.get(url2 + game_url,
	  headers={
	    "X-Mashape-Key": "Ug4hutuQNzmshzdMN8dNqV6v7Yi8p10pmmejsnKJl5NdrIzRMP"
	  }
	)


	if ("reviews" in response.body):
		num_results = 0
		for review in response.body['reviews']:
			num_results+=1
			if(review['name'] not in reviewers):
				reviewers[review['name']] = list()
			reviewers[review['name']].append(review)
			games[name].append(review)
		print "		got " + str(num_results) + " reviews"



#Import stuff.
def addReviewers(game, name):
	response = unirest.get(url + "pc%2F" + game,
	  headers={
	    "X-Mashape-Key": "Ug4hutuQNzmshzdMN8dNqV6v7Yi8p10pmmejsnKJl5NdrIzRMP"
	  }
	)


	if ("reviews" in response.body):
		num_results = 0
		for review in response.body['reviews']:
			num_results+=1
			if(review['name'] not in reviewers):
				reviewers[review['name']] = list()
			reviewers[review['name']].append(review)
			games[name].append(review)
		print "		got " + str(num_results) + " reviews"



def getReviewsFromSearch(title):
	response = unirest.post("https://byroredux-metacritic.p.mashape.com/search/game",
	  headers={
	    "X-Mashape-Key": "Ug4hutuQNzmshzdMN8dNqV6v7Yi8p10pmmejsnKJl5NdrIzRMP",
	    "Content-Type": "application/x-www-form-urlencoded"
	  },
	  params={
	    "max_pages": 1,
	    #"platform": 3,
	    "retry": 4,
	    "title": title
	  }
	)

	if("results" in response.body):
		for game in response.body["results"]:
			if(game["name"] not in games and 'rlsdate' in game and '2013' in game['rlsdate']):
				games[game["name"]] = list()
				name = game["name"].lower().replace(" ", "-").replace(":", "").replace("'", "")
				print("	getting reviews from " + name)
				#addReviewers(name, game["name"])
				addReviewersNonSelective(name, game["url"], game["name"])

import json
def Write():
	f = open('databases/reviewsAll.json', 'w')
	f.write(json.dumps(reviewers))


loadGames('databases/games.json')
for name in games_to_test:
	print("searching " + name.encode('utf-8'))
	getReviewsFromSearch(name)
	Write()

print "Pulled Down " + str(len(reviewers)) + " reviews."

