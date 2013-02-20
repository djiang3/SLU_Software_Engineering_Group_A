from __future__ import division
import time
import json
import zmq
import sys
import pprint
import numpy

# companies in DB : sony, sprint, verizon, samsung

if __name__ == "__main__":
      if (len(sys.argv) != 6):
            print "Format arguments as tweet_trender.py serverAddress keyword year month day, please"
            exit()

company = sys.argv[2]
year = sys.argv[3]
month = sys.argv[4]
day = sys.argv[5]
dateRange = year + '-' + month + '-' + day

# connect to zmq  
context = zmq.Context()  
socket = context.socket(zmq.REQ)   
address = ("tcp://%s:5555" % sys.argv[1])  
print "connecting to server %s" % address  
socket.connect(address)

# format and send data package to zmq server
dataset = {'type' : "tweet_pull", 'company' : company, 'dateRange' : dateRange}
message = json.dumps(dataset)
socket.send(message)

message = socket.recv()
rcvd = json.loads(message)

numTweets = len(rcvd)
score = 0

for row in rcvd:
      if (row[3] == 'pos'):
            score += 1
      else:
            score += -1
            
avgScore = score/numTweets
print "%s scored an average sentiment of %f" % (company, avgScore)

dataset = {'type' : 'avgSentiment_push', 'dateRange' : dateRange, 'company' : company, 'dataType' : 'avgSentiment', 'sentiment' : avgScore, 'volume' : numTweets}
message = json.dumps(dataset)
socket.send(message)
