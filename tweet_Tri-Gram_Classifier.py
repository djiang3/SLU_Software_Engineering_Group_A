from __future__ import division
from math import *
import nltk
from nltk.metrics import *
import json
import zmq
from sentiment_analyzer import date_convert
from sentiment_analyzer import month_to_num
from datetime import datetime
import time, calendar

# The use of the term 'trigram' in this file is arbritrary, and can represent either unigram, bigram, or trigram functionality.
# Currently this classifier uses bigrams.

jsonFile = open("master_tweet_sample.json")

jsonString = jsonFile.read()
tweetRawData = json.loads(jsonString)
jsonFile.close()

tweetCounter = 0
testList = []
trainList = []
testSentimentDict = dict()
testTextDict = dict()

allTrigrams = ""
posTrigrams = ""
neuTrigrams = ""
negTrigrams = ""

for _dict in tweetRawData:
    if (tweetCounter < 500):
        testSentimentDict[_dict['id']] = _dict['sentiment']
        testTextDict[_dict['id']] = _dict['text']
        # ^^^ unigram
        
        #textArray = _dict['text'].split()
        #bigrams = ""
        #for i in range(len(textArray)):
         #   bigram = ""
          #  if (i > 0):
           #     bigram = textArray[i-1] + textArray[i]
            #bigrams += bigram + " "
        #testTextDict[_dict['id']] = bigrams
        # ^^^ bigram
        
        testList.append(_dict['id'])
        tweetCounter += 1
    else:
        trainList.append(_dict['id'])
        textArray = _dict['text'].split()
        trigrams = ""    
        for i in range(len(textArray)):
            #trigram = ""
            #if (i > 1):
                #trigram = textArray[i-2] + textArray[i-1] + textArray[i]
            #trigrams += trigram + " "
            # ^^^ trigram
            
            #trigram = ""
            #if (i > 0):
             #   trigram = textArray[i-1] + textArray[i]
            #trigrams += trigram + " "
            # ^^^ bigram
            
            trigram = textArray[i]
            trigrams += trigram + " "
            # ^^^ unigram
            
        tweetCounter += 1
        sentiment = _dict['sentiment']
        if (sentiment == "positive"):
            posTrigrams += trigrams
        elif (sentiment == "negative"):
            negTrigrams += trigrams
        else:
            neuTrigrams += trigrams  

posTrigramListX = []
negTrigramListX = []
neuTrigramListX = []
posTrigramsX = ""
negTrigramsX = ""
neuTrigramsX = ""
posTrigramList = posTrigrams.split()
negTrigramList = negTrigrams.split()
neuTrigramList = neuTrigrams.split()

for trigram in posTrigramList:
    if (posTrigramList.count(trigram) > 0): posTrigramListX.append(trigram)
for trigram in negTrigramList:
    if (negTrigramList.count(trigram) > 0): negTrigramListX.append(trigram)
for trigram in neuTrigramList:
    if (neuTrigramList.count(trigram) > 0): neuTrigramListX.append(trigram)
    

for trigram in posTrigramListX:
    posTrigramsX += " " + trigram
for trigram in negTrigramListX:
    negTrigramsX += " " + trigram
for trigram in neuTrigramListX:
    neuTrigramsX += " " + trigram

trainDict = dict()
trainDict['positive'] = posTrigrams
trainDict['negative'] = negTrigrams
trainDict['neutral'] = neuTrigrams

trainDictX = dict()
trainDictX['positive'] = posTrigramsX
trainDictX['negative'] = negTrigramsX
trainDictX['neutral'] = neuTrigramsX

trainCFD = nltk.ConditionalFreqDist(
    (sentiment, trigram)
    for sentiment in trainDictX.keys()
    for trigram in trainDictX[sentiment].split())



actualScoreList = []
testScoreList = []

print "Analyzing %d total tri-grams." % trainCFD.N()
print "There are %d postively rated trigrams." % trainCFD['positive'].N()
print "There are %d negatively rated trigrams." % trainCFD['negative'].N()
print "There are %d neutrally rated trigrams." % trainCFD['neutral'].N()

print trainCFD.keys()

# Create a port for recieving data on port 5556 (for get_tweets.py) 
contextIN = zmq.Context()
socketIN = contextIN.socket(zmq.REP)
socketIN.bind("tcp://*:5556")

# Connect to the zmq server and prepare it to send data                     
contextOUT = zmq.Context()
socketOUT = contextOUT.socket(zmq.REQ)
socketOUT.connect("tcp://localhost:5555")

# Begin processing tweets from the get_tweets client.

while True:
    print "Waiting to recieve a message"
    messageIN = socketIN.recv()
    rcvd = json.loads(messageIN)
    print "Message accepted, processing"
    
    for tweet in rcvd:
        
        # Handler for tweet_send type.
        if tweet['type'] == "tweet_send":

            date = date_convert(tweet)
            best = -9999
            win = 'none'
        
            for rating in trainCFD.keys():
                logProb = 0
                for word in tweet['text'].split():
                    logProb += log( ((trainCFD[rating][word] + 0.001)/(trainCFD[rating].N() + 0.001)) * (trainCFD[rating].N()/trainCFD.N()))
                if (logProb > best):
                    best = logProb
                    win = rating
                    
                    # Formatted JSON that will be sent to the server.
                    data_set = {'type': "tweet_push", 'company':tweet["company"], 'date': date, 'sentiment' : win, 'id' : tweet["id"],'tweet' : tweet['text']}

                    # Send data to the zmq server
                    messageOUT = json.dumps(data_set)
                    socketOUT.send(messageOUT)
                    messageOUT = socketOUT.recv()

        # Shutdown protocol.
        elif rcvd['type'] == "tweet_stop":
            print "Recieved tweet_stop."
            print "Shutting down..."
            socketIN.send("Ack")
            
            sys.exit()

        else:
            # Send reply back to client that the query is unspecified.  
            print "received unknown query, ignoring"
            socketIN.send("Ack")

    socketIN.send("Ack")

i = 0

for tweetID in testList:
    if (testScoreList[i] != actualScoreList[i]):
        print actualScoreList[i] + " : " + testScoreList[i] + "    " + testTextDict[tweetID]
        print i
    i += 1

print len(testScoreList)
print len(actualScoreList)
cm = ConfusionMatrix(testScoreList, actualScoreList)
print cm

score = 0
for i in range(len(actualScoreList)):
    if (testScoreList[i] == actualScoreList[i]):
        score += 1
overallScore = (score/len(testScoreList)) * 100

print "Overall accuracy is ", overallScore, "%."

