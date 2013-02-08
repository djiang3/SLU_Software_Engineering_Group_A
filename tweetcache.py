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
	def __init__(self, tweet, company, weight=1, isFriend=False):
		self.tweet = tweet
		self.weight = weight
		self.company = company
		self.isFriend = isFriend
		
	def asDict(self):
		tweetDict = self.tweet.AsDict()
		tweetDict['weight'] = self.weight
		tweetDict['isFriend'] = self.isFriend
		tweetDict['company'] = self.company
		return tweetDict


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
		self.friendTweets = []

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
			friendTimeline = []

                        for id in range(len(friends)):
				#does not affect remainingHits
				friendTimeLine = self.api.GetFriendsTimeline(user=friends[id].id, since_id=self.sinceID)
                                self.updateRateLimitInfo()
				
				for ftw in friendTimeline:
					self.friendTweets.append(WeightedTweet(ftw, friends[id].screen_name, weight=2, isFriend=True))

                #get tweets relating to companies
		print '...Adding tweets from search...'

		positiveTweets = dict()
		positiveTweets['tweets'] = []
		positiveTweets['companies'] = []
		negativeTweets = dict()
		negativeTweets['tweets'] = []
		negativeTweets['companies'] = []
		financialTweets = dict()
		financialTweets['tweets'] = []
		financialTweets['companies'] = []

                for c in self.companies:
			if(self.positiveTerms):
				for i in self.positiveTerms:
					searchTerm = c + ' ' + i
                               		positiveTweets['tweets'].append(self.api.GetSearch(term=searchTerm, since_id=self.sinceID, per_page=DEFAULT_PAGE_LENGTH))
					positiveTweets['companies'].append(c)
                               		self.updateRateLimitInfo()
				#positiveTweets['companies'].append(c)
			if(self.negativeTerms):
				for i in self.negativeTerms:
					searchTerm = c + ' ' + i
                               		negativeTweets['tweets'].append(self.api.GetSearch(term=searchTerm, since_id=self.sinceID, per_page=DEFAULT_PAGE_LENGTH))
					negativeTweets['companies'].append(c)
                               		self.updateRateLimitInfo()
				#negativeTweets['companies'].append(c)
			if(self.financialTerms):
				for i in self.financialTerms:
					searchTerm = c + ' ' + i
                               		financialTweets['tweets'].append(self.api.GetSearch(term=searchTerm, since_id=self.sinceID, per_page=DEFAULT_PAGE_LENGTH))
					financialTweets['companies'].append(c)
                               		self.updateRateLimitInfo()
				#financialTweets['companies'].append(c)

#		print len(positiveTweets['companies'])
#		print len(positiveTweets['tweets'])
#		sys.exit(1)


		for i in range(len(positiveTweets['companies'])):
			for j in range(len(positiveTweets['tweets'][i-1])):
				self.weightedTweets.append(WeightedTweet(positiveTweets['tweets'][i-i][j-1], positiveTweets['companies'][i-1]))
		for i in range(len(negativeTweets['companies'])):
			for j in range(len(negativeTweets['tweets'][i-1])):
				self.weightedTweets.append(WeightedTweet(negativeTweets['tweets'][i-i][j-1], negativeTweets['companies'][i-1]))
		for i in range(len(financialTweets['companies'])):
			for j in range(len(financial['tweets'][i-1])):
				self.weightedTweets.append(WeightedTweet(financialTweets['tweets'][i-1][j-1], financialTweets['companies'][i-1]))

                #update sinceID to latest tweet
                self.sinceID = self.weightedTweets[len(self.weightedTweets)-1].tweet.id

	#trouble getting correct rate limit info
	def updateRateLimitInfo(self):
		rateLimitStatus = self.api.GetRateLimitStatus()
		self.resetTime = rateLimitStatus[RESET_TIME]
		self.remainingHits = rateLimitStatus[REMAINING_HITS]

	def getSearchTweets(self):
		return self.weightedTweets

	def getFriendTweets(self):
		return self.friendTweets

	def getTweetsAsDicts(self):
		fullTweetDict = []
		for wt in self.weightedTweets:
			fullTweetDict.append(wt.asDict())
		if(self.useFriends):
			for ft in self.friendTweets:
				fullTweetDict.append(ft.asDict())
		return fullTweetDict

	def getCreationTime(self):
		return self.creationTime

	def getSinceID(self):
		return self.sinceID

