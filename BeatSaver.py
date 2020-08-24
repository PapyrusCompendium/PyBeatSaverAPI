import json
import math
import urllib
import urllib.request

apiResource = "https://new.scoresaber.com/api"
webHeaders = {'User-Agent': 'Mozilla/5.0'}

def GetResource(endpoint):
    try:
        return urllib.request.urlopen(urllib.request.Request(f"{apiResource}{endpoint}", headers = webHeaders)).read().decode("utf-8")
    except:
        return ""

def GetUser(userID):
    return json.loads(GetResource(f"/player/{userID}/full"))

def GetScores(userID):
    userStats = GetUser(userID)
    pageCount = math.ceil(userStats['scoreStats']['totalPlayCount'] / 8)
    print(f"Downloading {pageCount} pages...")

    allScores = json.loads(GetResource(f"/player/{userID}/scores/recent/1"))
    for pageNumber in range(2, pageCount):
        print(f"Downloading Page {pageNumber}")
        jsonData = GetResource(f"/player/{userID}/scores/recent/{pageNumber}")
        allScores['scores'] += (json.loads(jsonData)['scores'])
    return allScores

userID = 11111111111111111 #Use your player ID here.
userStats = GetUser(userID)

print(f"All user stats:\n{userStats}")
print(f"Player Name: {userStats['playerInfo']['playerName']}")

scores = GetScores(userID)
print(f"Finished downloading all {len(scores['scores'])} scores for {userStats['playerInfo']['playerName']}")