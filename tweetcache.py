import twitter
import time
import sys
import json
import os
import urllib
import datetime
import zmq


#string constants
S_ID='id_str'
S_RESULTS='results'
S_TWEET_QUERY = "http://search.twitter.com/search.json?q="
S_RESULTS_PER_PAGE="&rpp=100"
S_SINCE_ID="&since_id="

#numeric constants
N_RESULTS_PER_PAGE=100


class WeightedTweet:
	def __init__(self, tweet, company, weight=1):
		self.tweet = tweet
		self.weight = weight
		self.company = company
		self.type = 'tweet_send'

	def __eq__(self, other):
		return self.getTweetText() == other.getTweetText()
		
	def asDict(self):
		tempDict = dict()
		tempDict['weight'] = self.weight
		tempDict['company'] = self.company
		tempDict['type'] = self.type
		fullDict = dict(self.tweet.items() + tempDict.items())
		return fullDict


	def getTweetText(self):
		return self.tweet['text']

	#returns ID as string
	def getTweetID(self):
		return self.tweet['id_str']

	def getTweetUsername(self):
		return self.tweet['from_user']

	def getTweetUserID(self):
		return self.tweet['from_user_id_str']

	#returns date of tweet as datetime instance
	def getTweetDate(self):
		return self.tweet['created_at']


	def getTweetRecipient(self):
		return self.tweet['to_user_id_str']


	
class TweetCacheError(Exception):
	
	@property
	def message(self):
		return self.args[0]


class TweetCache:
	def __init__(self, api, companies, sinceID="0", weightedTweets=[], creationTime=0, tweetCountTotal=0):
		self.api = api
		self.companies = companies
		self.sinceID = sinceID
		self.weightedTweets = weightedTweets
		self.creationTime = creationTime
		self.tweetCountTotal = tweetCountTotal

		self.initializeCache()


	def initializeCache(self):

		self.creationTime = time.time()

		if(isinstance(self.sinceID, str) == False):
			raise TweetCacheError("SinceID must be a string")
			sys.exit(1)
				
	def updateCache(self):

                #get tweets relating to companies
		self.clearCache()

		tweets = []

                for c in self.companies:
			query = self.generateQuery(c)
                        search = urllib.urlopen(query)
			tweets = json.loads(search.read())
			try:
				for pt in tweets[S_RESULTS]:
					self.weightedTweets.append(WeightedTweet(pt, c))
			except KeyError:
				raise TweetCacheError("Could not find any positive tweets")
	

                #update sinceID to latest tweet
		if(len(self.weightedTweets) > 0):
                	self.sinceID = self.weightedTweets[0].asDict()[S_ID]


	def getTweetsAsDicts(self):
		if(len(self.weightedTweets) > 0):
			allTweetDict = []
			for wt in self.weightedTweets:
				allTweetDict.append(wt.asDict())
			return allTweetDict
		else:
			raise TweetCacheError("No new tweets found")

	def getTweets(self):
		if(len(self.weightedTweets) > 0):
			return self.weightedTweets
		else:
			raise TweetCacheError("No new tweets found")

	def sendToServer(self, context, tweetDict):
		#try:
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:5556")
                message = json.dumps(tweetDict)
                socket.send(message)
                message = socket.recv()
		#except Error:
		#	raise TweetCacheError("Could not send info to server")

	def getCreationTime(self):
		return self.creationTime

	def getSinceID(self):
		return self.sinceID

	def generateQuery(self, c):
		return S_TWEET_QUERY+c+'+'+S_RESULTS_PER_PAGE+S_SINCE_ID+self.sinceID

	#number of tweets currently in cache
	def getTweetCount(self):
		return len(self.weightedTweets)
	
	def getCompanies(self):
		return self.companies

	#number of tweets that gone through cache
	def getTweetCountTotal(self):
		if(self.tweetCountTotal == 0):
			return len(self.weightedTweets)
		return self.tweetCountTotal

	def clearCache(self):
		self.tweetCountTotal = self.tweetCountTotal + len(self.weightedTweets)
		self.weightedTweets = []

