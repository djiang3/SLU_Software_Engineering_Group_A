# A simple tweet searching program that takes in a search query and sends a dictionary of the id of the tweet, the text of the tweet, the time the tweet was created, and the data type so that it is recognized by the analyzer program.

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize import line_tokenize
import os, bz2, sys
import urllib, getyql, sqlite3, zmq
import json, simplejson
import csv
import time
import twitter, tweetcache

# Function for submitting and storing a search query to a list with a tweet tuple consisting of an id, text, and time stamp.
def searchTweets(query):
    temp_list = list()
    search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
    dict = json.loads(search.read())
    
    # Code for specifying specific fields to include from the tweet.
    """
    for result in dict["results"]: # result is a list of dictionaries
        tweet = result["id"],result["text"], result["created_at"]
        temp_list.append(tweet)
    return temp_list """

    return dict

def connect(): 

    # Connect to the zmq server.                                                    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:5556")

def send():

    # Code that enables sent data to contain a more specific field for the object.
    """
    for tweet in tweets:                                             
        tweet_data = {'type': "tweet_send", 'id':tweet[0], 'text':tweet[1], 'date'\:tweet[2]}                                     
        print "sending tweet id: ", tweet[0]                                  
        message = json.dumps(tweet_data)                                            
        """
    message = json.dumps(tweets)
    socket.send(message)
    message = socket.recv()

# Decrypt the keys for the twitter API
def decrypt():
    fname = 'encrypted.txt'
    try:
        eKeys = [line.strip() for line in open(fname)]
    except IOError as e:
        print "IOError({0}): {1}".format(e.errno, e.strerror)
        sys.exit(1)

    dKeys = [bz2.decompress(k) for k in eKeys]


    return dKeys


# Load the API
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

# Simple search with sentiment key words and financial keywords
def keyword_search(company):

    tweet_dict = dict()
    tweets = searchTweets(name+"+good&rpp=100")
    
    searchTweets(name+"+great&rpp=100")
    searchTweets(name+"+cool&rpp=100")
    searchTweets(name+"+awesome&rpp=100")
    searchTweets(name+"+love&rpp=100")
    searchTweets(name+"+happy&rpp=100")
    searchTweets(name+"+nice&rpp=100")
    searchTweets(name+"+thank&rpp=100")

    searchTweets(name+"+bad&rpp=100")
    searchTweets(name+"+awful&rpp=100")
    searchTweets(name+"+terrible&rpp=100")
    searchTweets(name+"+suck&rpp=100")
    searchTweets(name+"+unhappy&rpp=100")
    searchTweets(name+"+poor&rpp=100")
    searchTweets(name+"+never&rpp=100")
    searchTweets(name+"+hate&rpp=100")
    
    searchTweets(name+"+business&rpp=100")
    searchTweets(name+"+money&rpp=100")
    searchTweets(name+"+finance&rpp=100")

# Processes the search query and send the data to the analyzer server, marked as a tweet_push data type.
def main():

    if(len(sys.argv) < 2):
        print 'usage: get_tweets.py COMPANY [COMPANY COMPANY...]'
        sys.exit(1)

    companies = []
    for c in range(len(sys.argv)-1):
        companies.append(sys.argv[c+1])

    keys = decrypt()

    print 'initializing api...'
    api = initializeAPI(keys)

    positiveTerms = {'good','great', 'awesome', 'cool', 'love', 'happy', 'nice', 'thank', 'fantastic', 'satisfaction'}
    negativeTerms = {'bad', 'awful', 'terrible', 'suck', 'unhappy', 'poor', 'hate', 'never', 'poor'}
    financialTerms = {'business', 'money', 'finance'}

    print 'initializing tweet cache...'

    try:
        cache = tweetcache.TweetCache(api, companies, positiveTerms=positiveTerms, negativeTerms=negativeTerms, financialTerms=financialTerms)
    except twitter.TwitterError:
        print "Could not authenticate API. Make sure all authentication keys are correct"
        sys.exit(1)

    cache.updateCache()
    tweet_dict = cache.getTweetsAsDicts()

    # Output the query into a json file.
    manual_dict = json.dumps(tweet_dict)
    manual_tweet_sample = open('manual_tweet.json','w')
    manual_tweet_sample.write(manual_dict)

    print "Search file created: manual_tweet.json"
    manual_tweet_sample.close

if __name__ == '__main__':
    main()

