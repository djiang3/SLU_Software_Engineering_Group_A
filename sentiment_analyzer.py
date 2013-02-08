# A baby version of the sentiment analyzer.

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus.reader import WordListCorpusReader
import os

#Specify the directory of your data for your unique corpora. 
#Test code, the foundation for using our own corpora to train the classifier.
os.chdir("/Users/nltk_data/corpora/tweet_reviews")
tweet_review = nltk.corpus.reader.CategorizedPlaintextCorpusReader('.','.*\.txt', cat_pattern='(\w+)/*')

def review_features(review):
    return dict([(review, True) for review in review])
 
negIDs = movie_reviews.fileids('neg')
posIDs = movie_reviews.fileids('pos')
 
negReview = [(review_features(movie_reviews.words(fileids=[id])), 'neg') for id in negIDs]
posReview = [(review_features(movie_reviews.words(fileids=[id])), 'pos') for id in posIDs]
 
trainSet = negReview[:len(negReview)] + posReview[:len(posReview)]

print "Training on ", len(trainSet), "individual files..."
 
sentimentClassifier = NaiveBayesClassifier.train(trainSet)

# Analyzes all tweets in the specified files and outputs the file name and its sentiment value.
for files in os.listdir("."):
  if (files != '.DS_Store'):
		
    #specify the directory for processing.
    path = ('corpora/tweet_reviews/'+files)
		
		load = nltk.data.load(path, format='raw')
		tokens = word_tokenize(load)
		features = review_features(tokens)
		print files,': ',sentimentClassifier.classify(features)
		
