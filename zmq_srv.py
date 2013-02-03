#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#
import zmq
import time
import sqlite3
import getyql
import json
import pprint

#connect to zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
 
#connet to database
sdb = getyql.simpledb()
c = sdb.conn.cursor()

while True:
    #  Wait for next request from client
    message = socket.recv()
    rcvd = json.loads(message)

    #  Do some 'work'
    time.sleep (1)        #   Do some 'work'

    # interpret the query and run database operation
    if rcvd['type'] == "stock_push":
      # did we receive a raw stock value to store?
      print "stock push request received for %s from %s" % (rcvd['symbol'], rcvd['clientname'])
      c.execute("INSERT INTO stocks VALUES (NULL, %d, '%s', '%s')" % (rcvd['timestamp'], rcvd['symbol'], rcvd['price']))
      sdb.conn.commit()
      print "added %s into database" % rcvd['symbol']
      socket.send("Ack")
    elif rcvd['type'] == "stock_pull":
      print "stock pull request received for %s from %s" % (rcvd['symbol'], rcvd['clientname'])
      pulled_stocks = []
      for row in c.execute("SELECT * FROM stocks WHERE symbol = '%s' order by timestamp" % rcvd['symbol']):
        pulled_stocks.append(row)
      message = json.dumps(pulled_stocks)
      socket.send(message)
    else:
      #  Send reply back to client
      print "received unknown query, ignoring"
      socket.send("Ack")
