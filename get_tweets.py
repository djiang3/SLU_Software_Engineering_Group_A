import twitter
import bz2
import time
import sys
import tweetcache

#compressed with bz2. definitely insecure but not human readable in file
def decrypt():
	fname = 'encrypted.txt'
	eKeys = [line.strip() for line in open(fname)]
	dKeys = [bz2.decompress(k) for k in eKeys]

	return dKeys
	

#load api
def initializeAPI(keys):
	cKey = keys[0]
	csKey = keys[1]
	atKey = keys[2]
	atsKey = keys[3]

	try:
		api = twitter.Api(consumer_key=cKey, \
				consumer_secret=csKey, \
				access_token_key=atKey, \
				access_token_secret=atsKey)
		return api
	except twitter.TwitterError:
		print "API could not be loaded"
		sys.exit(1)

def main():

	keys = decrypt()

	print 'initializing api...'
	api = initializeAPI(keys)

	myCompanies = {'Apple', 'Google', 'Yahoo', 'Target'}

	print 'initializing tweet cache...'
	cache = tweetcache.TweetCache(api, myCompanies, useFriends=True)
	allCacheTweets = cache.getCompanyTweets()

	for t in allCacheTweets:
		print t.tweet.user.screen_name
		print t.tweet.text


if __name__ == '__main__':
	main()
