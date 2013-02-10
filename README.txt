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

### Populating your stock database
If the database isn't already created, run "python getyql.py"

The easiset way to generate data for analysis is to pull historical daily 
stock information for a specific ticker symbol. zmq_loaddaily.py was written
to do just that! This program will take a ticker symbol, a start date, and an
end date, and download the daily stock values for each trading day within
that range inclusive of the dates given.


Database Info
----------------
Timestamp information should be stored as a string now. When pulling
historical stock data, this timestamp should include a date in text format
"YYYY-MM-DD HH:MM", OR "YYYY-MM-DD high" OR "YYYY-MM-DD low". 
