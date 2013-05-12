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

To populate the database with sorted tweet information, you must run 
tweet_Tri-Gram_Classifier. This is then followed by the get_tweets.py program which
will take in a company name(s) as its search term. get_tweets.py will output a raw
tweet object to the tweet_Tri-Gram_Classifier, which will then process the 
information and store into the database a formatted dictionary with:
   1) "id" of the tweet.
   2) "date" of the tweet, which is the creation date of that tweet.
   3) "sentiment" of the tweet, either positive or negative.
   4) "company" that the tweet is refering to. 
   5) "tweet" which is the text of the tweet.

Database Info
----------------
Timestamp information should be stored as a string now. When pulling
historical stock data, this timestamp should include a date in text format
"YYYY-MM-DD HH:MM", OR "YYYY-MM-DD high" OR "YYYY-MM-DD low". 

Supplementary Tools
________________
A few tools have been created to enable the users a greater degree in flexibility
with the corpora they want to use in order to train the sentiment analyzer which
are as follows:

### sanders_tweet_corpora_extractor ###

This tool is focused primarily on Sander's twitter corpora which contains roughly
4000 usable, individually sorted tweets with categories of positive, negative, and
neutral. This tool will take the supplied information Sander's corpora download 
and distill the csv and rawdata into a more usable format, such as a json or a text 
file. Just stick this program into the folder where you installed Sander's corpora.

USAGE: "python sanders_tweet_corpora_extractor <mode>"

The modes are as follows:
    -jM (For a json of all sentiments)
    -jS (For separate jsons of positive, negative, and neutral)
    -txtM (For a text file of all sentiments)
    -txtS (For separate text files of positive, negative, and neutral)

### search_tweets ###

Search tweets is a program built to supply data for a user in use with either the
json_filter or the text_filter manual sorting programs. This program will
create a single json named "manual_tweet.json" with the keyword a user specifies.
With this keyword, search_tweets will attempt to search twitter for all tweets with
that keyword including a scattering of positive, negative, and financial terms to
zone in on possibly useful tweets.

USAGE: "python search_tweets.py <keyword>"

### text_filter ###

The text filter manual sorting program is built for the purpose of supplying the
nltk trainer with more data. text filter will display the text of a tweet, provide
the various options for sorting, and build several text files of the respective 
sentiment.

USAGE: "python text_filter.py"

       z = Positive
       x = Negative
       c = Trash
       a = Useful Trash
       q = Save and Quit
       [Enter] to skip the tweet

### json_filter ###

The json filter manual sorting program is built for the purpose of supplying 
training data for the tri_gram sentiment classifier. json filter will take the
manual_tweet.json file and traverse, one by one, each tweet object. It will display
the text for the user and allow the user to sort into either positive, negative,
neutral, or trash. json_filter will create 4 files, 1 for positive, negative, neutral,
and 1 for the master json that contains all 3 of these sentiments. Json filter will
also append a sentiment key to the tweet object before writing it to the file.

USAGE: "python json_filter.py"
       z = Positive
       x = Negative
       c = Neutral
       a = Trash
       q = Save and Quit
       [Enter] to skip the tweet.

### json_toolkit ###

The json toolkit is meant to handle a few necessities when dealing with jsons. 
Currently, it includes two functionalities, which is merging two jsons together
and checking the integrity of a json file.

USAGE: "python json_toolkit [-m fileA fileB newFileName] [-c file] "
       -m: merges fileA and fileB, then outputs the combined file as newFileName
       -c: checks the integrity of a json file


