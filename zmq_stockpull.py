import time
import json
import zmq
import sys
import pprint

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "usage: zmq_stockpull.py TICKER [TICKER TICKER...]"
    exit()

  pprint.pprint(sys.argv)

  tickers = []

  for itr in range( len(sys.argv)-1 ):
    tickers.append(sys.argv[itr+1])

  # connect to zmq
  print "connecting to server..."
  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  socket.connect ("tcp://localhost:5555")

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
    pprint.pprint(rcvd)
