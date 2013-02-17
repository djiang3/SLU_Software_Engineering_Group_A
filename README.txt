Group A Readme
--------------


This is our readme!
Hooray!

Link to python-twitter downloads: https://github.com/bear/python-twitter/wiki
Link to Twitter documentation: https://dev.twitter.com/docs


Getting Started
---------------
The entire system centers around zmq_srv.py, this is the server that
hosts the database that the individual clients will connect to and 
expect to do a number of things, from pushing tweets and stocks to from 
repsective APIs, to pulling existing tweets and stocks for analysis, to
storing that analysis

start the server with "python zmq_srv.py"
If the database isn't already created, run "python getyql.py"

### Populating your stock database

The easiset way to generate data for analysis is to pull historical daily 
stock information for a specific ticker symbol. zmq_loaddaily.py was written
to do just that! This program will take a ticker symbol, a start date, and an
end date, and download the daily stock values for each trading day within
that range inclusive of the dates given.

### Populating your tweet database

To populate the database with tweet information, you must run 
sentiment_analyzer.py. This is then followed by the get_tweets.py program which
will take in a company name as its search term. get_tweets.py will output a raw
tweet object to the sentiment_analyzer, which would then process the 
information and store into the database a formatted dictionary with:
   1) "id" of the tweet.
   2) "date" of the tweet, which is the creation date of that tweet.
   3) "sentiment" of the tweet, either positive or negative.
   4) "company" that the tweet is refering to. 

Database Info
----------------
Timestamp information should be stored as a string now. When pulling
historical stock data, this timestamp should include a date in text format
"YYYY-MM-DD HH:MM", OR "YYYY-MM-DD high" OR "YYYY-MM-DD low". 
