import getyql
import yql
import time
import json
import zmq
import sys
import pprint

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "usage: zmq_stockpush.py ADDR TICKER [TICKER TICKER...]"

  pprint.pprint(sys.argv)

  tickers = []

  for itr in range( len(sys.argv)-2 ):
    tickers.append(sys.argv[itr+2])

  # connect to zmq
  y = getyql.getyql()
  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  addr = ("tcp://%s:5555" % sys.argv[1])
  print "connecting to server %s" % addr
  socket.connect (addr)

  for request in range (10):
    for stock in tickers:
      #request google
      result = y.Instant(stock)
      timestamp = time.time()

      # format data package
      dataset = {'type' : "stock_push", 'symbol' : result[0]["symbol"], 'price' : result[0]["AskRealtime"], 'timestamp' : timestamp, 'clientname':'Steve'}
      message = json.dumps(dataset)
      pprint.pprint(dataset)

      # send data package
      print "Sending stock ", request, ", ticker ", stock, "..."
      socket.send(message)

      # wait for reply
      message = socket.recv()
      print "Received reply ", request, "[", message, "]"

