from __future__ import division
import time
import json
import zmq
import sys
import pprint
import numpy

def main(serverAddress, company):
      #company = sys.argv[2]
      #year = sys.argv[3]
      #month = sys.argv[4]
      #day = sys.argv[5]
      #dateRange = year + '-' + month + '-' + day
      
      # connect to zmq  
      context = zmq.Context()  
      socket = context.socket(zmq.REQ)   
      address = ("tcp://%s:5555" % serverAddress)  
      print "connecting to server %s" % address  
      socket.connect(address)
      
      # format and send data package to zmq server
      dataset = {'type' : "tweet_pull", 'company' : company}
      message = json.dumps(dataset)
      socket.send(message)
      
      message = socket.recv()
      rcvd = json.loads(message)
      
      numTweets = len(rcvd)
      dailyNumTweets = dict()
      dailyAverage = dict()
      dailyPositive = dict()
      dailyNeutral = dict()
      dailyNegative = dict()
      
      for row in rcvd:
         if row['date'] in dailyNumTweets.keys():
            if (row[3] == 'pos'):
               dailyPositive[row['date']] += 1
               dailyAverage[row['date']] += 1
               dailyNumTweets[row['date']] += 1
            elif (row[3] == 'neg'):
               dailyNegative[row['date']] += 1
               dailyAverage[row['date']] += 1
               dailyNumTweets[row['date']] += 1               
            else:
               dailyNeutral[row['date']] += 1
               dailyNumTweets[row['date']] += 1
         else:
            dailyPositive[row['date']] = 0
            dailyNegative[row['date']] = 0
            dailyNeutral[row['date']] = 0
            dailyAverage[row['date']] = 0
            dailyNumTweets[row['date']] = 0
            
            if (row[3] == 'pos'):
               dailyPositive[row['date']] += 1
               dailyAverage[row['date']] += 1
               dailyNumTweets[row['date']] += 1
            elif (row[3] == 'neg'):
               dailyNegative[row['date']] += 1
               dailyAverage[row['date']] += 1
               dailyNumTweets[row['date']] += 1               
            else:
               dailyNeutral[row['date']] += 1
               dailyNumTweets[row['date']] += 1            

      for date in dailyNumTweets.keys():
         avgScore = dailyAverage[date]/dailyNumTweets[date]
         print "%s scored an average sentiment of %f on %s" % (company, avgScore,date)
      
         dataset = {'type' : 'avgSentiment_push', 'dateRange' : date, 'company' : company, 'averageValue' : avgScore, 'positive' : dailyPositive[date], 'negative' : daliyNegative[date], 'neutral' : dailyNeutral[date], 'dataVolume' : dailyNumTweets[date]}
      
         message = json.dumps(dataset)
         socket.send(message)


if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])

