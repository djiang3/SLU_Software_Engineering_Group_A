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

class graphanalysis:
  def __init__(self, rcvd, rcvd_type):
    # initialize variable
    self.rcvd_type = rcvd_type
    
    # process json packet into usable data
    if rcvd_type = 'stock':
      self.process_json(rcvd)
    else if rcvd_type = 'tweet':
      pass
    else
      raise Exception("Invalid graph type created")
  
    xs = pylab.arange(0, len(self.dtarr), 1)

  def process_json_stock(self, rcvd):
    # processes json packet of information
    # add a zero element so we can perform array operations
    self.arr = np.array([0])
    self.dtarr = np.array([0])
    # include just the averages
    for row in rcvd:  
      if st.find(row[1], "avg")>0:
        dt = datetime.strptime(row[1][:10],'%Y-%m-%d')
        self.dtarr = np.vstack((dtarr, [dt]))
        self.arr = np.vstack((arr, [row[3]]))   # [row[0], row[1], row[2], row[3]]))
      else:
        pass
    
    self.arr = np.delete(arr, 0)
    self.dtarr = np.delete(dtarr, 0)

  def process_json_tweet(self, rcvd):
    # process json packet of daily tweet sentiment data
 
  def interpolate(self):
    # run graph anaylsis

    # make iterator values over length of date array
    xs = pylab.arange(0, len(self.dtarr), 1)

    # polynomial fit of the graph we have (this time just use 10)
    self.coeff = polyfit(xs,self.arr,10)
    self.polynom = poly1d(coeff)
    self.ys = polynom(xs)

  def run_plot(self):
    pylab.plot_date(self.dtarr, self.arr, 'o')
    pylab.plot_date(self.dtarr, self.ys, '-')
    pylab.ylabel('y')
    pylab.xlabel('x')

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

    stk = graphanalysis(rcvd, 'stock')
    stk.interpolate()
    stk.run_plot()
