import getyql
import yql
import time
import json
import zmq
import sys

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "usage: zmq_stockpush.py TICKER [TICKER TICKER...]"

  pprint.pprint(sys.argv)

  exit()

  # connect to zmq
  print "connecting to server..."
  y = getyql.getyql()
  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  socket.connect ("tcp://localhost:5555")

  for request in range (10):
    #request google
    result = y.Instant("GOOG")
    timestamp = time.time()

    # format data package
    dataset = {'type' : "stock_push", 'symbol' : result[0]["symbol"], 'price' : result[0]["AskRealtime"], 'timestamp' : timestamp}
    message = json.dumps(dataset)

    # send data package
    print "Sending stock ", request, "..."
    socket.send(message)

    # wait for reply
    message = socket.recv()
    print "Received reply ", request, "[", message, "]"
