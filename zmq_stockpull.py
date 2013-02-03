import time
import json
import zmq
import sys
import pprint

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "usage: zmq_stockpull.py TICKER [TICKER TICKER...]"
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
    pprint.pprint(rcvd)
