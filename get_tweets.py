import twitter
import bz2
import time
import sys
import tweetcache
import json
import urllib2
import zmq
import pickle
import os
import re

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

def saveCacheState(cache):

	#TODO catch try and catch failed save error
	cacheInfoDict = dict()
        cacheInfoDict['companies'] = cache.getCompanies()
        cacheInfoDict['sinceID'] = cache.getSinceID()
        cacheInfoDict['creationTime'] = cache.getCreationTime()
        cacheInfoDict['tweetCountTotal'] = cache.getTweetCountTotal()

	try:
        	cacheInfoDict['tweets'] = cache.getTweetsAsDicts()
	except tweetcache.TweetCacheError as e:
		cacheInfoDict['tweets'] = []
		print e.message
	
	currentTime = time.time()
	pickleString = "CacheSavePickle:{0}.p".format(currentTime)
	pickle.dump(cacheInfoDict, open(pickleString, "wb"))

	return 0

def loadCacheState(api, companies=[]):
	cache = 0
	pl = 0
	file = 0
	files = os.listdir(".")
	for f in files:
		if re.match("CacheSavePickle", f):
			file = f
			p = open(f, 'rb')
			pl = pickle.load(p)
			break

	print "Loaded pickle: {0}".format(file)
	if(pl != 0):
		if companies:
			pl['companies'].extend(companies)
		try:
			cache = tweetcache.TweetCache(api, pl['companies'], sinceID=str(pl['sinceID']), creationTime=pl['creationTime'], tweetCountTotal=pl['tweetCountTotal'], weightedTweets=pl['tweets'])
		except tweetcache.TweetCacheError as e:
			print e.message
			print "Failed to create cache from pickle"
			sys.exit(1)

			
	return cache

def removePickles():
	files = []
	for file in os.listdir("."):
		if re.match("CacheSavePickle", file):
			files.append(file)
	for f in files:
		os.remove(f)
	return 0


def main():

	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		print 'usage: get_tweets.py "COMPANY [COMPANY COMPANY...]" [-p]'
		sys.exit(1)

	print 'initializing api...'
	keys = decrypt()
	api = initializeAPI(keys)

	companies = []
	pickleCache = 0

	#read command line input
	if(len(sys.argv) == 2 and sys.argv[1] != "-p" ):
		companies = sys.argv[1].split(' ')
	elif(len(sys.argv) == 3 and (sys.argv[1] == "-p" or sys.argv[2] == "-p")):
		i = sys.argv.index('-p')
		companies = sys.argv[3-i].split(" ")
		for company in companies:
			company = company.replace('_', ' ')
		pickleCache = loadCacheState(api, companies=companies)

	#remove previous pickle
	removePickles()

	#check network connection
	if(checkNetworkConnection() == False):
		print "No network connection detected"
		sys.exit(1)

	context = zmq.Context()

	print 'initializing tweet cache...'

	cache = 0
	if(pickleCache == 0):
		try:
			cache = tweetcache.TweetCache(api, companies)
		except twitter.TwitterError:
			print "Could not authenticate API. Make sure all authentication keys are correct"
			sys.exit(1)
	else:
		cache = pickleCache
		cache.setInitialized(True)

	#if search returns empty 3 times in a row, cut out
	timesBlank = 0
	sleepTime = 10

	print "Connecting to network..."
	while(1):
		try:
			if(checkNetworkConnection() == True):
				print "Searching for tweets..."
				try:
					if(cache.isInitialized() == True):
						cache.updateCache()
					else:
						cache.initializeCache()
				except tweetcache.TweetCacheError as e:
					print e.message

				print "Search returned {0} tweets...".format(cache.getTweetCount())

				try:
					tweet_dict = cache.getTweetsAsDicts()
					print "Sending tweet dictionary..."
					
					try:
						cache.sendToServer(context, tweet_dict)
					except tweetcache.TweetCacheError as e:
						print e.message
						sys.exit(1)

					print "Sent!"
				except tweetcache.TweetCacheError as e:
					print e.message 
					timesBlank = timesBlank+1
			
				if(timesBlank == 3):
					print "Search was unsuccessful, sleeping for 30 min"
					sleepTime = 600
					#sleepTime = 30
					timesBlank = 0

			time.sleep(sleepTime)
			sleepTime = 10

		except KeyboardInterrupt:
			print "Saving Cache..."
			saveCacheState(cache)
			print "Cache Saved..."

			print "\nStopping Sentiment Analyzer"
			stopDict = {'type':"tweet_stop"}
			cache.sendToServer(context, stopDict)
			
			exit(1)
		
	#TODO send to analyzer


if __name__ == '__main__':

	main()
