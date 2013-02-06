# stock_importdaily.py
# steve massey
#
# imports daily stock information from YQL database
# given at ticker symbol and a date range 
#
# data is sent to the given address where presumably a zmq_srv.py
# server is running on the other end

import getyql
import yql
import json
import zmq
import sys
import pprint
from datetime import datetime, date, time
import cStringIO
import csv


if __name__ == "__main__":
  if len(sys.argv) < 8:
    print "usage: zmq_stockpush.py ADDR TICKER mm_start dd_start yy_start mm_end dd_end yy_end"
    print "  ADDR - address of target zmq_srv.py server"
    print "  TICKER - ticker symbol to retreive info on"
    print "  mm_start - two-digit month for beginning of date range"
    print "  dd_start - two-digit day for beginning of date range"
    print "  yy_start - four-digit year for beginning of date range"
    print "  mm_end - two-digit month for end of date range"
    print "  dd_end - two-digit day for end of date range"
    print "  yy_end - four-digit year for end of date range"
    exit()
  pprint.pprint(sys.argv)
  ticker = sys.argv[2]

  print int(sys.argv[5]), int(sys.argv[3]), int(sys.argv[4])
  print int(sys.argv[8]), int(sys.argv[6]), int(sys.argv[7])
  # connect to zmq
  y = getyql.getyql()
  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  addr = ("tcp://%s:5555" % sys.argv[1])
  print "connecting to server %s" % addr
  socket.connect (addr)

  y = getyql.getyql()
  d1 = date( int(sys.argv[5]), int(sys.argv[3]), int(sys.argv[4]) )
  d2 = date( int(sys.argv[8]), int(sys.argv[6]), int(sys.argv[7]) )
  out = y.CSVGrab( ticker, d1, d2, 'd')
  out = cStringIO.StringIO(out)

  sheet = csv.reader(out)
  for row in sheet:
    # generate two stock push queries from each row:
    #   open, close, mid-day
    #   open is at 9:30am
    #   close is at 4pm
    #print row
    if row[0] == "Date":
      print "title row; moving to next one"
      pass
    else:
      # get our times
      time_raw = datetime.strptime(row[0], "%Y-%m-%d").date()
      time_open = datetime.combine(time_raw, time(9, 30))
      time_close = datetime.combine(time_raw, time(16,00)) 
      
      
      # dataset for market open
      dataset = {'type' : "stock_push", 'symbol' : ticker, 'price' : row[1] , 'timestamp' : time_open.strftime("%Y-%m-%d %H:%M"), 'clientname' : "csv_grab"}
      print "Sending stock ", ticker, " on ", time_open.strftime("%Y-%m-%d %H:%M")
      message = json.dumps(dataset)
      socket.send(message)

      message = socket.recv()
      print "received reply [",message,"]"

      # dataset for market close
      dataset = {'type' : 'stock_push', 'symbol' : ticker, 'price' : row[4] , 'timestamp' : time_close.strftime("%Y-%m-%d %H:%M"), 'clientname' : 'csv_grab'}
      print "Sending stock ", ticker, " on ", time_close.strftime("%Y-%m-%d %H:%M")
      message = json.dumps(dataset)
      socket.send(message)

      message = socket.recv()
      print "received reply [",message,"]"

