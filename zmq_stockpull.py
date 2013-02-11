import time
import json
import zmq
import sys
import pprint
import numpy as np
import string as st

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "usage: zmq_stockpull.py ADDR TICKER [TICKER TICKER...]"

    pprint.pprint(sys.argv)
    exit()


  tickers = []

  for itr in range( len(sys.argv)-2 ):
    tickers.append(sys.argv[itr+2])

  # connect to zmq
  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  addr = ("tcp://%s:5555" % sys.argv[1])
  print "connecting to server %s" % addr
  socket.connect ( addr )

  for stock in tickers:

    # format data package
    dataset = {'type' : "stock_pull", 'symbol' : stock, 'clientname' : 'Steve'}
    message = json.dumps(dataset)
    pprint.pprint(dataset)

    # send data package
    print "Requesting data for ticker ", stock, "..."
    socket.send(message)

    # wait for reply
    message = socket.recv()
    print "Received reply for ticker ", stock

    # print retreived stocks
    rcvd = json.loads(message)    
    #pprint.pprint(rcvd)

    arr = np.array([0,0,0,0])

    for row in rcvd:
      if st.find(row[1], "avg")>0:
        pass
        #print "ignoring average value"
        #arr = np.vstack((arr, [row[0], row[1], row[2], row[3]]))
      else:
        arr = np.vstack((arr, [row[0], row[1], row[2], row[3]]))
      """
      if st.find(row[1], "high")>0:
        print "ignoring high value"
      elif st.find(row[1], "low")>0:
        print "ignoring low value"
      else:
        arr = np.vstack((arr, [row[0], row[1], row[2], row[3]]))
      """
    print arr[-30:]


