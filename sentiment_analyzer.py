
"""Sentiment analyzer that uses the Naive Bayes Classifier algorithm for classification along with the nltk movie_review corpora. 

In its current state, it searches through a certain directory, analyzes all the text files in that directory and sends it to the zmq database with a dictionary value of its type and the sentiment rating."""


import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus.reader import WordListCorpusReader
import yql, json, zmq, os, sqlite3, getyql
import pprint, urllib, csv
import time, calendar
from datetime import datetime
from time import strptime
import pickle, sys

# Foundation code to incorporate our unique set of corpora, used to train the Naive Bayes Classifier on usefulness of a tweet and the sentiment of the tweet. This code will not be used until we begin to create are own data set for the trainer."""
#os.chdir("/Users/DJiang/nltk_data/corpora/movie_reviews/neg")
#tweet_review = nltk.corpus.reader.CategorizedPlaintextCorpusReader('.','.*\.txt', cat_pattern='(\w+)/*')

# Feature set function that builds a dictionary from the reviews, with a value of either positive or negative, followed by the corresponding tweet.            
def review_features(review):
    return dict([(review, True) for review in review])

# Function that will take in an abbreviated month name and output a string that corresponds to its number value. 
# *RETURNS* a num representation of the month as a string
def month_to_num(month):
    months_dict = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04", "May":"05", "Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    return months_dict[month]

# Function that takes in a tweet object dictionary, finds the date of creation of that tweet, and converts it into a more usable datetime python object.
# *RETURNS* a datetime object in isoformat
def date_convert(tweet_dict):
    date_tokens = (tweet_dict["created_at"]).split()
    
    date_str = list()

    # Appends year (YYYY)
    date_str.append(date_tokens[3]) 
    # Appends month (MM)
    date_str.append(month_to_num(date_tokens[2]))
    # Appends day (DD)
    date_str.append(date_tokens[1])
    # Appends time (HH:MM:SS)
    date_str.append(date_tokens[4])

    # Creates a string: (YYYY-MM-DD-HH:MM:SS)
    raw_date = '-'.join(date_str)

    # Creates datetime in format (YYYY-MM-DD HH:MM:SS)
    date_obj = datetime(*strptime(raw_date, "%Y-%m-%d-%H:%M:%S")[0:6])
    
    # Returns datetime in format (YYYY-MM-DDTHH:MM:SS)
    return date_obj.isoformat()

# Function that takes in a tweet object dictionary and a classifer and then classifies the the text of the tweet, depending on the classifier.
# *RETURNS* a classification
def classify(tweet_dict,classifier):
    text_tokens = word_tokenize(tweet_dict["text"])
    features = review_features(text_tokens)
    classification = classifier.classify(features)
    return classification

# Function that loads a classifier pickle and sets a new classifer to it.
# *RETURNS* a classifier from the pickle.
def load_pickle(old_pickle):
    relish = open(old_pickle)
    classifier = pickle.load(relish)
    relish.close()
    return classifier

def main():
	
    # Create a port for recieving data on port 5556 (for get_tweets.py)
    contextIN = zmq.Context()
    socketIN = contextIN.socket(zmq.REP)
    socketIN.bind("tcp://*:5556")

    # Connect to the zmq server and prepare it to send data
    contextOUT = zmq.Context()
    socketOUT = contextOUT.socket(zmq.REQ)
    socketOUT.connect("tcp://localhost:5555")

    # Counters to demonstrate positve / negative sentiments
    pos_cnt = 0
    neg_cnt = 0
    
    # Load the classifier.
    print "Loading sentiment.pickle..."
    s_classifier = load_pickle('sentiment.pickle')
    print "Loading complete. Waiting for input..."

    # Run the server to accept data from get_tweet and send data to zmq_srv.
    while True:
	
        # Wait for the next request from the client and load the message.
        messageIN = socketIN.recv()
        rcvd = json.loads(messageIN)
        print "Sending data to server..."
        
        try:
            # Handler for tweet_send type.
            for tweet in rcvd:
	
                # Handler for the "tweet_send" type 
                if tweet['type'] == "tweet_send":
	
                    date = date_convert(tweet)
                    sentiment = classify(tweet, s_classifier)   

                    data_set = {'type': "tweet_push", 'company':tweet["company"], 'date': date, 'sentiment' : sentiment, 'id' : tweet["id"],'tweet' : tweet['text'] }
				
                    if(sentiment == 'pos'):
                        pos_cnt += 1
                    else:
                        neg_cnt += 1

                    # Send data to the zmq server
                    messageOUT = json.dumps(data_set)
                    socketOUT.send(messageOUT)
                    messageOUT = socketOUT.recv()     
   

                else:
                    # Send reply back to client that the query is unspecified.
                    print "received unknown query, ignoring"
                    socketIN.send("Ack") 

            # Send reply back to get_tweet indicating file has been sent.
            print "Message sent successfully."
            print "positive/negative:(",pos_cnt,"/",neg_cnt,")"
            socketIN.send("Ack")

        except:
            # Handles the dictionary sent to end the process and end the program.
            if (rcvd['type'] == "tweet_stop"):
                print "Recieved tweet_stop."
                print "Shutting down..."
		socketIN.send("Ack")
                
                sys.exit()


# Analyzes all tweets in the specified directory and sends the data to the zmq server through port 5555. Sends a dictionary value of its type and the corresponding sentiment rating.
"""
for files in os.listdir("."):
    if (files != '.DS_Store'):
        path = ('corpora/movie_reviews/neg/'+files)
        load = nltk.data.load(path, format='raw')
        tokens = word_tokenize(load)
        features = review_features(tokens)
        
        t = files, sentimentClassifier.classify(features)
        data_set = { 'sentiment' : sentimentClassifier.classify(features), 'type':"tweet_push"}
        message = json.dumps(data_set)
        
        pprint.pprint(data_set)
        socket.send(message)
        message = socket.recv()
"""


if __name__ == '__main__':
    main()


