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
	def __init__(self, api, companies, sinceID="0", positiveTerms=None, negativeTerms=None, financialTerms=None):
		self.api = api
		self.companies = companies
		self.sinceID = sinceID
		self.positiveTerms = positiveTerms
		self.negativeTerms = negativeTerms
		self.financialTerms = financialTerms
		self.creationTime = 0
		self.resetTime = 0
		self.remainingHits = 0
		self.weightedTweets = []

		self.initializeCache()


	def initializeCache(self):

		#set creation time
		self.creationTime = time.time()

		if(isinstance(self.sinceID, str) == False):
			raise TweetCacheError("SinceID must be a string")
			sys.exit(1)
				
		#self.updateCache()


	def updateCache(self):

                #get tweets relating to companies
		self.weightedTweets=[]

		positiveTweets = []
		negativeTweets = []
		financialTweets = []

                for c in self.companies:
			if(self.positiveTerms):
				#not O(n^3) because of limited search terms
				#can be improved if needed
				for i in self.positiveTerms:
					query = self.generateQuery(c,i)
                               		positiveSearch = urllib.urlopen(query)
					positiveTweets = json.loads(positiveSearch.read())
					try:
						for pt in positiveTweets[S_RESULTS]:
							self.weightedTweets.append(WeightedTweet(pt, c))
					except KeyError:
						raise TweetCachError("Could not find any positive tweets")
					#else:
					#	raise TweetCacheError("End of positive tweets")
	
			if(self.negativeTerms):
				for i in self.negativeTerms:
					query = self.generateQuery(c,i)
					negativeSearch = urllib.urlopen(query)
					negativeTweets = json.loads(negativeSearch.read())
					try:
						for nt in negativeTweets[S_RESULTS]:
							self.weightedTweets.append(WeightedTweet(nt, c))
					except KeyError:
						raise TweetCacheError("Could not find any negative tweets")

			if(self.financialTerms):
				for i in self.financialTerms:
					query = self.generateQuery(c,i)
					financialSearch = urllib.urlopen(query)
					financialTweets = json.loads(financialSearch.read())
					try:
						for ft in financialTweets[S_RESULTS]:
							self.weightedTweets.append(WeightedTweet(ft, c))
					except KeyError:
						raise TweetCacheError("Could not find any financial tweets")

                #update sinceID to latest tweet
		if(len(self.weightedTweets) > 0):
                	self.sinceID = self.weightedTweets[0].asDict()[S_ID]
			#print self.sinceID
			#print self.weightedTweets[0].asDict()[S_ID]


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

	def generateQuery(self, c, t):
		return S_TWEET_QUERY+c+'+'+t+S_RESULTS_PER_PAGE+S_SINCE_ID+self.sinceID

	def getTweetCount(self):
		return len(self.weightedTweets)

	def clearCache(self):
		self.weightedTweets = []

