import twitter
import bz2
import time
import sys
import tweetcache
import json
import urllib2


def checkNetworkConnection():
	try:
		connect = urllib2.urlopen('http://www.google.com/')
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

	keys = decrypt()

	print 'initializing api...'
	api = initializeAPI(keys)

	positiveTerms = {'good', 'great', 'awesome', 'cool', 'love'}

	print 'initializing tweet cache...'

	try:
		cache = tweetcache.TweetCache(api, companies, positiveTerms=positiveTerms)
	except twitter.TwitterError:
		print "Could not authenticate API. Make sure all authentication keys are correct"
		sys.exit(1)

	allCacheTweetDict = cache.getTweetsAsDicts()
	for dict in allCacheTweetDict:
		print dict['text'].encode(encoding='UTF-8')

	#TODO send to analyzer


if __name__ == '__main__':
	main()
