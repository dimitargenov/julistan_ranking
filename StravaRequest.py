import requests

class StravaRequest():
	url = ""
	headers = {}

	def __init__(self, url, headers):
		self.url = url
		self.headers = headers

	def getLeaderboard(self):
		return requests.request("GET", self.url, headers=self.headers)    

        
# requests.request("GET", self.url, headers=self.headers)
#def getLeaderboardFromStrava(self):
    #    return requests.request("GET", self.url, headers=self.headers)    
    #def getLeaderboardFromStrava(self):
    #    return requests.request("GET", self.url, headers=self.headers)

    #def makeCalculations(self, leaderboard):
    #    for row in leaderboard.json()['data']:
    #        print(row.distance)
    #        exit()  