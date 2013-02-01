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
      c.execute("INSERT INTO stocks VALUES (NULL, %d, '%s', '%s')" % (rcvd['timestamp'], rcvd['symbol'], rcvd['price']))
      sdb.conn.commit()
      print "added %s into database" % rcvd['symbol']
    else:
      print "received unknown query, ignoring"

    #  Send reply back to client
    socket.send("Ack")
