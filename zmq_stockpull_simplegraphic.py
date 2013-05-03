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
if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "usage: zmq_stockpull.py ADDR TICKER [TICKER TICKER...]"

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

    # print retreived st5ocks
    rcvd = json.loads(message)    
    pprint.pprint(rcvd)

    arr = np.array([0])
    dtarr = np.array([0])
    for row in rcvd:  
      if st.find(row[1], "avg")>0:
        dt = datetime.strptime(row[1][:10],'%Y-%m-%d')
        dtarr = np.vstack((dtarr, [dt]))
        arr = np.vstack((arr, [row[3]]))   # [row[0], row[1], row[2], row[3]]))
        #pass
        #print "ignoring average value"
        #arr = np.vstack((arr, [row[0], row[1], row[2], row[3]]))
      else:
        pass
        #arr = np.vstack((arr, [row[0], row[1], row[2], row[3]]))
      """
      if st.find(row[1], "high")>0:
        print "ignoring high value"
      elif st.find(row[1], "low")>0:
        print "ignoring low value"
      else:
        arr = np.vstack((arr, [row[0], row[1], row[2], row[3]]))
      """
    #dtarr_plot = matplotlib.dates.date2num(dtarr)
    #plot_date fusses if there's a zero-value in the date array
    arr = np.delete(arr, 0)
    dtarr = np.delete(dtarr, 0)

    #print 'arr', arr[:20]
    #print len(arr)

    #print 'dtarr', dtarr[:20]
    #print len(dtarr)
    #for i in arr

    xs = pylab.arange(0, len(dtarr), 1)
    #f = interpolate.splrep(xs,arr)
    #print f
    """
    # curve fitting, find the equation
    xs = pylab.arange(0, len(dtarr), 1)
    coeff = pylab.polyfit(arr, xs, 1)
    poly = pylab.poly1d(coeff)
    ys = pylab.poly(xs)
    """

    #print 'xs', xs[:-20]
    #print len(xs)

    coeff = polyfit(xs,arr,10)
    polynom = poly1d(coeff)
    ys = polynom(xs)

    #print 'ys', ys[:-20]
    #print len(ys)

    pylab.plot_date(dtarr, arr, 'o')
    pylab.plot_date(dtarr,ys, '-')
    pylab.ylabel('y')
    pylab.xlabel('x')

    print "coefficents are: ", coeff

    #pylab.plot(arr)
    pylab.show()
