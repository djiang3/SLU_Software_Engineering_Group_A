import twitter
import time
import sys
import json
import sqlite3
import zmq
import os
import urllib


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
		
	def asDict(self):
		tempDict = dict()
		tempDict['weight'] = self.weight
		tempDict['company'] = self.company
		fullDict = dict(self.tweet.items() + tempDict.items())
		return fullDict



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
				
		print '...Performing initial fill...'
		self.updateCache()


	def updateCache(self):

                #get tweets relating to companies
		print '...Adding tweets from search...'

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
					for pt in positiveTweets[S_RESULTS]:
						self.weightedTweets.append(WeightedTweet(pt, c))
	
			if(self.negativeTerms):
				for i in self.negativeTerms:
					query = self.generateQuery(c,i)
					negativeSearch = urllib.urlopen(query)
					negativeTweets = json.loads(negativeSearch.read())
					for nt in negativeTweets[S_RESULTS]:
						self.weightedTweets.append(WeightedTweet(nt, c))

			if(self.financialTerms):
				for i in self.financialTerms:
					query = self.generateQuery(c,i)
					financialSearch = urllib.urlopen(query)
					financialTweets = json.loads(financialSearch.read())
					for ft in financialTweets[S_RESULTS]:
						self.weightedTweets.append(WeightedTweet(ft, c))

                #update sinceID to latest tweet
		print self.sinceID
                self.sinceID = self.weightedTweets[len(self.weightedTweets)-1].asDict()[S_ID]
		print self.sinceID


	def getTweetsAsDicts(self):
		allTweets = []
		for wt in self.weightedTweets:
			allTweets.append(wt.asDict())
		return allTweets
			

	def getCreationTime(self):
		return self.creationTime

	def getSinceID(self):
		return self.sinceID

	def generateQuery(self, c, t):
		return S_TWEET_QUERY+c+'+'+t+S_RESULTS_PER_PAGE+S_SINCE_ID+self.sinceID

	def getTweetCount(self):
		return len(self.getTweetsAsDicts())

