from pylab import *
from datetime import datetime, date
import time
import json
import zmq
import sys
import pprint
import numpy as np
from scipy import interpolate
import pylab
import string as st
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.finance import candlestick
from matplotlib.dates import num2date
from matplotlib.dates import date2num

class graphanalysis:
  def __init__(self):
  # empty constructor


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "usage: graphanalysis ADDR TICKER [TICKER TICKER..]"

    pprint.pprint(sys.argv)
    exit()

  tickers = []

  for itr in range( len(sys.argv)-2 ):
  tickers.append(sys.argv[itr+2])

  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  addr = ("tcp://%s:5555" % sys.argv[1])
  print "connecting to server %s" % addr
  socket.connect( addr )

  for stock in tickers:

    # format data package
    dataset = {'type' : 'stock_pull', 'symbol' : stock, 'clientname' : 'graphanalysis_test'}
    message = json.dumps(dataset)
    pprint.pprint(dataset)

    # send data package
    print "Requesting data for ticker ", stock, "..."
    socket.send(message)

    # wait for reply
    message = socket.recv()
    print "Received reply for ticker ", stock

    # decode reply
    rcvd = json.loads(message)

    graphanalysis.graphanalysis()
