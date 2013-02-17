import twitter
import bz2
import time
import sys
import tweetcache
import json
import urllib2
import zmq

def checkNetworkConnection():
	try:
		connect = urllib2.urlopen('http://www.google.com/', timeout=1)
		return True
	except urllib2.URLError as ue:
		return False
	

def decrypt():
	fname = 'encrypted.txt'
	try:
		eKeys = [line.strip() for line in open(fname)]
	except IOError as e:
		print "IOError({0}): {1}".format(e.errno, e.strerror)
		sys.exit(1)

	dKeys = [bz2.decompress(k) for k in eKeys]


	return dKeys
	

#load api
def initializeAPI(keys):
	try:
		cKey = keys[0]
		csKey = keys[1]
		atKey = keys[2]
		atsKey = keys[3]
	except IndexError:
		print "InitializeAPI requires array of 4 Twitter OAuth keys"
		sys.exit(1)

	api = twitter.Api(consumer_key=cKey, \
			consumer_secret=csKey, \
			access_token_key=atKey, \
			access_token_secret=atsKey)
	return api

def main():

	if(len(sys.argv) < 2):
		print 'usage: get_tweets.py COMPANY [COMPANY COMPANY...]'
		sys.exit(1)
	
	companies = []
	for c in range(len(sys.argv)-1):
		companies.append(sys.argv[c+1])

	#check network connection
	if(checkNetworkConnection() == False):
		print "No network connection detected"
		sys.exit(1)

	context = zmq.Context()

	keys = decrypt()

	print 'initializing api...'
	api = initializeAPI(keys)

	positiveTerms = {'great', 'awesome', 'cool', 'love', 'happy', 'nice', 'thank'}
	negativeTerms = {'bad', 'awful', 'terrible', 'suck', 'unhappy', 'poor', 'hate'}
	financialTerms = {'business', 'money', 'finance'}

	print 'initializing tweet cache...'

	try:
		cache = tweetcache.TweetCache(api, companies, positiveTerms=positiveTerms, negativeTerms=negativeTerms, financialTerms=financialTerms)
	except twitter.TwitterError:
		print "Could not authenticate API. Make sure all authentication keys are correct"
		sys.exit(1)

	#print cache.getTweets()[0].getTweetDate()

	#if search returns empty 3 times in a row, cut out
	timesBlank = 0
	sleepTime = 10

	print "Connecting to network..."
	while(1):

		if(checkNetworkConnection() == True):
			print "Searching for tweets..."
			cache.updateCache()
			print "Search returned {0} tweets...".format(cache.getTweetCount())
			#print cache.getTweets()[cache.getTweetCount()-1].getTweetText()

			try:
				tweet_dict = cache.getTweetsAsDicts()
				print "Sending tweet dictionary..."

				try:
					cache.sendToServer(context, tweet_dict)
				except tweetcache.TweetCacheError as e:
					print e.message
					sys.exit(1)

				timesBlank = 0
				sleepTIme = 10
				print "Sent!"
			except tweetcache.TweetCacheError as e:
				print e.message 
				timesBlank = timesBlank+1
			
			if(timesBlank == 3):
				print "Search was unsuccessful, sleeping for 30 min"
				sleepTime = 600
				timesBlank = 0

		time.sleep(sleepTime)
		
	#TODO send to analyzer


if __name__ == '__main__':

	main()
