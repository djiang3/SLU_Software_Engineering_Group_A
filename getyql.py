# Retreives data using YQL
#
# Steve Massey - 1/21/13
#
# resources used:
# http://stackoverflow.com/questions/7625079/download-csv-directly-into-python-csv-parser
# http://stackoverflow.com/questions/376461/string-concatenation-vs-string-substitution-in-python
# http://code.google.com/p/yahoo-finance-managed/wiki/csvQuotesDownload
# may need http://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python

import simplejson as json
import urllib2
import pprint
import datetime
import cStringIO
import csv
import httplib2
import yql

def Instant(y, ticker):
  ## import instant quote
  query = "select symbol, AskRealtime from yahoo.finance.quotes where symbol in %s" % ticker
  result = y.execute(query)
  data = urllib2.urlopen(YQL)

  j = json.load(data)
  pprint.pprint(j)

def CSVGrab(ticker, start, stop, intv):
  ## string ticker; ticker symbol, string format
  ## date start;    start date of data to get, date object
  ## date stop;     end date of data to get, date object
  ## import CSV historical quote data
  ## http://code.google.com/p/yahoo-finance-managed/wiki/csvHistQuotesDownload
  url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&d=%s" % (ticker, (start.month-1), start.day, start.year, (stop.month-1), stop.day, stop.year, intv)
  h = httplib2.Http('.cache')
  headers, data = h.request(url)
  return data


if __name__ == "__main__":
  # todo: how to merge datasets. Yahoo only has day-by-day resolution
  # would be nice to have something with hour-by-hour at least?

  # demonstrate historical download
  d1 = datetime.date(2012,1,1)
  d2 = datetime.date(2012,6,1)
  out = CSVGrab('GOOG',d1,d2,'d')
  out = cStringIO.StringIO(out)

  sheet = csv.reader(out)
  for row in sheet:
    print row

  ## instant
  y = yql.Public()
  Instant(y,"goog")

