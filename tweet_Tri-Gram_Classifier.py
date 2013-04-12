from __future__ import division
from math import *
import nltk
from nltk.metrics import *
import json

jsonFile = open("master_tweet_sample.json")

jsonString = jsonFile.read()
tweetRawData = json.loads(jsonString)
jsonFile.close()

tweetCounter = 0
testList = []
trainList = []

posTrigrams = ""
neuTrigrams = ""
negTrigrams = ""

for _dict in tweetRawData:
    if (tweetCounter < 500):
        testList.append(_dict['id'])
    else:
        trainList.append(_dict['id'])
    textArray = _dict['text'].split()
    trigrams = ""    
    for i in range(len(textArray)):
        trigram = ""
        if (i > 1):
            trigram = textArray[i-2] + textArray[i-1] + textArray[i]
        trigrams += trigram + " "
    tweetCounter += 1
    sentiment = _dict['sentiment']
    print trigrams
    if (sentiment == "positive"):
        posTrigrams += trigrams
    elif (sentiment == "negative"):
        negTrigrams += trigrams
    else:
        neuTrigrams += trigrams  
    
trainDict = dict()
trainDict['positive'] = posTrigrams
trainDict['negative'] = negTrigrams
trainDict['neutral'] = neuTrigrams

trainCFD = nltk.ConditionalFreqDist(
    (sentiment, trigram)
    for sentiment in trainDict.keys()
    for trigram in trainDict[sentiment])


#actualScoreList = []

print "Analyzing %d total tri-grams." % trainCFD.N()
print "There are %d postively rated trigrams." % trainCFD['positive'].N()
print "There are %d negatively rated trigrams." % trainCFD['negative'].N()
print "There are %d neutrally rated trigrams." % trainCFD['neutral'].N()

print trainCFD.keys()

#for tweetID in tweetTestDict.keys():
    #actualScoreList += tweetTestDict
    