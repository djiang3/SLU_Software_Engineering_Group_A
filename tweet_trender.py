from __future__ import division
import time
import json
import zmq
import sys
import pprint
import numpy

#if __name__ == "__main__":
 #     if (len(sys.argv) != 6):
  #          print "Format arguments as tweet_trender.py serverAddress keyword year month day, please"
   #         exit()

# Format arguments as tweet_trender.py serverAddress keyword year month day, please
def tweetTrender(serverAddress, company, year, month, day):
      #company = sys.argv[2]
      #year = sys.argv[3]
      #month = sys.argv[4]
      #day = sys.argv[5]
      dateRange = year + '-' + month + '-' + day
      
      # connect to zmq  
      context = zmq.Context()  
      socket = context.socket(zmq.REQ)   
      address = ("tcp://%s:5555" % serverAddress)  
      print "connecting to server %s" % address  
      socket.connect(address)
      
      # format and send data package to zmq server
      dataset = {'type' : "tweet_pull", 'company' : company, 'dateRange' : dateRange}
      message = json.dumps(dataset)
      socket.send(message)
      
      message = socket.recv()
      rcvd = json.loads(message)
      
      numTweets = len(rcvd)
      average = 0
      positive = 0
      neutral = 0
      negative = 0
      score = 0
      
      for row in rcvd:
            if (row[3] == 'pos'):
                  positive += 1
                  average += 1
            elif (row[3] == 'neg'):
                  negative += 1
                  average += -1
            else:
                  neutral += 1
      
      avgScore = average/numTweets
      print "%s scored an average sentiment of %f" % (company, avgScore)
      
      dataset = {'type' : 'avgSentiment_push', 'dateRange' : dateRange, 'company' : company, 'averageValue' : avgScore, 'positive' : positive, 'negative' : negative, 'neutral' : neutral, 'dataVolume' : numTweets}
      
      message = json.dumps(dataset)
      socket.send(message)
