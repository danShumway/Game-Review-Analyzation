import urllib
import re

# Open wikipedia article contents
wikiContents = urllib.urlopen("http://en.wikipedia.org/wiki/2013_in_video_gaming")

# Extract only the Game Releases tables
gameReleaseContents = []
addStart = False

for w in wikiContents:
    # Look for the first table
    if not addStart:
        #if "id=\"Game_releases\"" in w:
        if "id=\"January.E2.80.93March\"" in w:
            addStart = True   
    else:
        gameReleaseContents.append(w)
        
        # Look for the end of the table; exit
        if "id=\"References\"" in w:
            break
        
# Extract only the tables' contents
tableContents = []
tableStart = False      
        
for item in gameReleaseContents:
    
    # Start extracting table content
    if not tableStart:
        if "<table" in item:
            tableStart = True
            
    # Continue extracting table content
    if tableStart:
        tableContents.append(item)
        
        # End extraction until next table
        if "</table>" in item:
            tableStart = False
    
        

# Remove the non-essential HTML tags
listWithHTML = []

for item in tableContents:
    # Remove the day of the month rows
    item = re.sub(r"<td rowspan.*", "", item)
    item = re.sub(r"<td>[0-9]*</td>", "", item)
    
    # Remove the months column
    item = re.sub(r".<br />", "", item)
    
    # Remove tags that take up a lot of space
    #item = re.sub(r"</?t[rd]>", "", item)
    #item = re.sub(r"</?i ?>", "", item)
    item = re.sub(r"\n", "", item)
    
    # Add back any non-empty strings    
    if len(item) > 0:
        listWithHTML.append(item)


# Pattern-matching fun
games = []
isTitle = False
game = None
platforms = None

for item in listWithHTML:
    # Handle the systems/platforms
    if isTitle:
        isTitle = False
        # Remove the remaining HTML tags
        item = re.sub(r"<[^>]*>", "", item)
        platforms = item.split(", ")

    # Handle the game titles
    if "<i>" in item:
        isTitle = True
        # Remove remaining HTML tags    
        item = re.sub(r"<[^>]*>", "", item)
        # Deal with hyphens
        item = re.sub(r"\xe2\x80\x93", "-", item)
        game = item
            
    # If found game and platform
    if game and platforms:
        games.append((game, platforms))
        game = None
        platforms = None
 
 
 #Write to file
import json
f = open('databases/games.json', 'w')
f.write(json.dumps(games))