#
#   A server to handle pushes and pulls of stock and tweet information.
#   Binds REP socket to tcp://*:5555
#   Expects a type from the client and will send a confirmation reply accordingly.
#
import zmq
import time
import sqlite3
import getyql
import json
import pprint

# Connect to the zmq server.
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
 
# Connect to the database.
sdb = getyql.simpledb()
c = sdb.conn.cursor()

# Have the server run forever.
while True:
	
    # Wait for the next request from the client and load the message.
    message = socket.recv()
    rcvd = json.loads(message)

    # Interpret the query based on its type value. The run the database operation accordingly.
    if rcvd['type'] == "stock_push":
      # did we receive a raw stock value to store?
      print "stock push request received for %s from %s" % (rcvd['symbol'], rcvd['clientname'])
      c.execute("INSERT INTO stocks VALUES (NULL, %d, '%s', '%s')" % (rcvd['timestamp'], rcvd['symbol'], rcvd['price']))
      sdb.conn.commit()
      print "added %s into database" % rcvd['symbol']
      socket.send("Ack")

	# Handler for stock_pull type.
    elif rcvd['type'] == "stock_pull":
      print "stock pull request received for %s from %s" % (rcvd['symbol'], rcvd['clientname'])
      pulled_stocks = []
      for row in c.execute("SELECT * FROM stocks WHERE symbol = '%s' order by timestamp" % rcvd['symbol']):
        pulled_stocks.append(row)
      message = json.dumps(pulled_stocks)
      socket.send(message)

    # Handler for tweet_push type.
    elif rcvd['type'] == "tweet_push":
        print "tweet recieved with a sentiment of %s" % (rcvd['sentiment'])
        c.execute("INSERT INTO tweets VALUES(NULL, '%s')" % (rcvd['sentiment']))
        sdb.conn.commit()
        print "added %s into database" % rcvd['sentiment']
        socket.send("Ack")
  
  	else:
      # Send reply back to client that the query is unspecified.
      print "received unknown query, ignoring"
      socket.send("Ack")



