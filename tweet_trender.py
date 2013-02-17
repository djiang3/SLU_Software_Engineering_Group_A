import time
import json
import datetime
import zmq
import sys
import pprint
import numpy

if __name__ == "__main__":
      if (len(sys.argv) != 4):
            print "Format arguments as tweet_trender.py serverAddress keyword daterange, please"
            exit()

company = sys.argv[1]
dateRange = sys.argv[2]

# connect to zmq  
context = zmq.Context()  
socket = context.socket(zmq.REQ)   
address = ("tcp://%s:5555" % sys.argv[1])  
print "connecting to server %s" % address  
socket.connect(address)

# format and send data package to zmq server
dataset = {'type' : "tweet_pull", 'company' : company, 'date_range' : dateRange }
message = json.dumps(dataset)
socket.send(message)

message = socket.recv()
rcvd = json.loads(message)

print message





