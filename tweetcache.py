import twitter
import time
import sys
import simplejson

#string constants
ID_INDEX='ids'
RESET_TIME='reset_time_in_seconds'
REMAINING_HITS='remaining_hits'

#numerical constants
DEFAULT_PAGES=10
DEFAULT_PAGE_LENGTH=100

class WeightedTweet:
	def __init__(self, tweet, weight=1):
		self.tweet = tweet
		self.weight = weight

class TweetCache:
	def __init__(self, api, companies, useFriends=False, sinceID=None, positiveTerms=None, negativeTerms=None, financialTerms=None):
		self.api = api
		self.companies = companies
		self.useFriends = useFriends
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
		
		#set remaining hits and time
		self.updateRateLimitInfo()
		
		print '...Performing initial fill...'
		self.updateCache()


	def updateCache(self):
		if(self.useFriends):
			print '...Adding friend timelines...'
                        friends = self.api.GetFriends()
                        initialTimeLines = []
                        for id in range(len(friends)):
				#does not affect remainingHits
				initialTimeLines.append(self.api.GetFriendsTimeline(user=friends[id].id, since_id=self.sinceID))
                                self.updateRateLimitInfo()
                        for timeline in initialTimeLines:
                                for tweet in timeline:
                                        self.weightedTweets.append(WeightedTweet(tweet, weight=2))

                #get tweets relating to companies
		print '...Adding tweets from search...'
		cTweets = []
                for c in self.companies:
			if(self.positiveTerms):
				for i in self.positiveTerms:
					searchTerm = c + ' ' + i
                               		cTweets.append(self.api.GetSearch(term=searchTerm, since_id=self.sinceID, per_page=DEFAULT_PAGE_LENGTH))
                               		self.updateRateLimitInfo()
			if(self.negativeTerms):
				for i in self.negativeTerms:
					searchTerm = c + ' ' + i
                               		cTweets.append(self.api.GetSearch(term=searchTerm, since_id=self.sinceID, per_page=DEFAULT_PAGE_LENGTH))
                               		self.updateRateLimitInfo()
			if(self.financialTerms):
				for i in self.financialTerms:
					searchTerm = c + ' ' + i
                               		cTweets.append(self.api.GetSearch(term=searchTerm, since_id=self.sinceID, per_page=DEFAULT_PAGE_LENGTH))
                               		self.updateRateLimitInfo()
		for c in cTweets:
			for t in c:
				self.weightedTweets.append(WeightedTweet(t))

                #update sinceID to latest tweet
                self.sinceID = self.weightedTweets[len(self.weightedTweets)-1].tweet.id
		

	#trouble getting correct rate limit info
	def updateRateLimitInfo(self):
		rateLimitStatus = self.api.GetRateLimitStatus()
		self.resetTime = rateLimitStatus[RESET_TIME]
		self.remainingHits = rateLimitStatus[REMAINING_HITS]

	def getCompanyTweets(self):
		#TODO enter company name and return tweets for that company
		return self.weightedTweets

	def getCreationTime(self):
		return self.creationTime

