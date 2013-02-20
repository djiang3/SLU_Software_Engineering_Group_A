# Corpora_trainer.py will create and output a classifier in the form of a pickle file. 

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus.reader import WordListCorpusReader
import pickle, sys

# Feature set function that builds a dictionary from the reviews, with a value of either positive or negative, followed by the corresponding tweet.
def review_features(review):
    return dict([(review, True) for review in review])

# Function that will take in the name of a corpora set(with positive and negative fields) and trains a classifier.
# *RETURNS* a classifier
def train_on(corpora):
    # Acquires the IDs of the reviews by its sentiment and stores them into neg ID and posIDs.                       
    negIDs = corpora.fileids('neg')
    posIDs = corpora.fileids('pos')
    
    #Creates a large dictionary based on review_features of negative and positive reviews.
    negReview = [(review_features(corpora.words(fileids=[id])), 'neg') for id in negIDs]
    posReview = [(review_features(corpora.words(fileids=[id])), 'pos') for id in posIDs]
    
    # Train the classifier with a populated training set of all positive and negative reviews in the movie_review corpora.
    trainSet = negReview[:len(negReview)] + posReview[:len(posReview)]
    print "Training on ", len(trainSet), "individual files..."

    #The Naive Bayes Classifer, using the trainSet to train.
    sentiment_classifier = NaiveBayesClassifier.train(trainSet)
    print "Training complete."
    return sentiment_classifier

# Function that takes in a corpora (sentiment based), trains a classifier, and saves this classifier as a pickle object.
# *OUTPUTS* a pickle file that can be loaded in an analyzer.
def create_pickle(corpora):
    
    new_classifier = train_on(movie_reviews)
    print "Building the pickle..."
    new_pickle = open('sentiment.pickle','wb')
    pickle.dump(new_classifier,new_pickle)
    new_pickle.close()
    print "Build successful."

def main():
    #if(len(sys.argv) < 2): 
     #   print 'usage: sentiment_analyzer.py [classifier]'
      #  sys.exit(1)
    
    create_pickle(movie_reviews)

if __name__ == '__main__':
    main()

	
	
