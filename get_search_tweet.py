# A simple tweet searching program that takes in a search query and sends a dictionary of the id of the tweet, the text of the tweet, the time the tweet was created, and the data type so that it is recognized by the analyzer program.

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize import line_tokenize
import os
import urllib
import json
import csv
import simplejson
import time
import sqlite3
import getyql
import yql
import zmq

# Function for submitting and storing a search query to a list with a tweet tuple consisting of an id, text, and time stamp.
def searchTweets(query):
 temp_list = list()
 search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
 dict = json.loads(search.read())
 #print dict["results"]
 return dict
"""
 for result in dict["results"]: # result is a list of dictionaries
     tweet = result["id"],result["text"], result["created_at"]
     temp_list.append(tweet)
 return temp_list
 """


name = "bestbuy"
tweet_dict = dict()
tweets = searchTweets(name+"+good&rpp=100")

# Connect to the zmq server.
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:5556")

#searchTweets(name+"+great&rpp=100")
#searchTweets(name+"+cool&rpp=100")
#searchTweets(name+"+awesome&rpp=100")
#searchTweets(name+"+love&rpp=100")
#searchTweets(name+"+happy&rpp=100")
#searchTweets(name+"+nice&rpp=100")
#searchTweets(name+"+thank&rpp=100")
#
#searchTweets(name+"+bad&rpp=100")
#searchTweets(name+"+awful&rpp=100")
#searchTweets(name+"+terrible&rpp=100")
#searchTweets(name+"+suck&rpp=100")
#searchTweets(name+"+unhappy&rpp=100")
#searchTweets(name+"+poor&rpp=100")
#searchTweets(name+"+never&rpp=100")
#searchTweets(name+"+hate&rpp=100")
#
#searchTweets(name+"+business&rpp=100")
#searchTweets(name+"+money&rpp=100")
#searchTweets(name+"+finance&rpp=100")
# Processes the search query and send the data to the analyzer server, marked as a tweet_push data type.

#for tweet in tweets:
 #   tweet_data = {'type': "tweet_send", 'id':tweet[0], 'text':tweet[1], 'date':tweet[2]}
  #  print "sending tweet id: ", tweet[0]


#message = json.dumps(tweet_data)
message = json.dumps(tweets)
socket.send(message)
message = socket.recv()
