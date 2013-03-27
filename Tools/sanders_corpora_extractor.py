# Program that enables the user to sift through Niek Sander's tweet corpora. Useful for converting and condensing the corpora and outputting:
	# A json file of positive, negative, and neutral or ALL sentiments.
	# A text file of only positive, negative, and neutral tweets or ALL tweets.

import csv, os, json
from pprint import pprint
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus.reader import WordListCorpusReader
import pickle, sys

#os.chdir('/export/mathcs/home/student/d/djiang3/csci390/sanders_twitter/')

# Build the index list that contain all of the classified tweet IDs and its respective sentiment rating from the corpus.csv.
def build_index():
	index_list = list()
	print "Building index_list..."
	try:
		with open('corpus.csv','rb') as csvfile:
			spamreader = csv.reader(csvfile)
			for row in spamreader:
				index_dict = {'id': row[2], 'sentiment': row[1]}
				index_list.append(index_dict)
				
		print "Index list constructed."
		return index_list
			
	except IOError:
		print "corpus.csv not found.\nFailed to build index list.\nExiting..."
		exit(1)

# Build a concise list of tweet dictionaries that includes the: text of the tweet, the id of the tweet, and the sentiment of the tweet.
# Traverses the index list and the files in the rawdata directory that contains all the tweet objects from sanders_twitter and adds a new dictionary value if the two tweet IDs match.
def build_dict(index_list):
	dict_list = list()
	print "Building dict_list..."
	# Change directory to rawdata, where all of the tweet objects are contained.
	fn = os.path.join(os.path.dirname(__file__), 'rawdata')
	os.chdir(fn)
	for file in os.listdir("."):
		if(file != '.DS_Store'):
			#print file
			msg = open(file)
			data = json.load(msg)
			for type in data:
				if(type == 'id_str'):
					for line in index_list:
						if(data['id_str'] == line['id']):
							temp_dict = {'text':data['text'], 'id': data['id_str'], 'sentiment': line['sentiment']}
							dict_list.append(temp_dict)
				msg.close()
	print "Dictionary list constructed."
	
	# Return to the main directory.
	os.chdir('..')
	
	return dict_list

# Output the converted corpora data as a json text file containing a dictionary of text, id, and sentiment.
def output_file(dict_list, mode):
	master_list = list()
	pos_list = list()
	neg_list = list()
	neu_list = list()
	
	for dict in dict_list:	master_list.append(dict)
	for dict in dict_list:
		if(dict['sentiment'] == 'positive'):
			pos_list.append(dict)
		if(dict['sentiment'] == 'negative'):
			neg_list.append(dict)
		if(dict['sentiment'] == 'neutral'):
			neu_list.append(dict)
	
	if(mode == '-jM'):
		master = json.dumps(master_list)
		master_tweet_sample = open('master_tweet_sample.json','a')
		master_tweet_sample.write(master+"\n")
		master_tweet_sample.close()
		
	elif(mode == '-jS'):
		pos_out = json.dumps(pos_list)
		neg_out = json.dumps(neg_list)
		neu_out = json.dumps(neu_list)
		
		positive_tweet_sample = open('positive_tweet_sample.json','a')
		negative_tweet_sample = open('negative_tweet_sample.json','a')
		neutral_tweet_sample = open('neutral_tweet_sample.json','a')
	
		positive_tweet_sample.write(pos_out+"\n")
		negative_tweet_sample.write(neg_out+"\n")
		neutral_tweet_sample.write(neu_out+"\n")
		
		positive_tweet_sample.close()
		negative_tweet_sample.close()
		neutral_tweet_sample.close()
		
	#elif(mode == '-txtM'):
		
	#elif(mode == '-txtS'):
	#	pos_out = '\n'.join(pos_list).encode('utf-8').strip()
	#	neg_out = '\n'.join(neg_list).encode('utf-8').strip()
	#	neu_out = '\n'.join(neu_list).encode('utf-8').strip()

def main():
	if(len(sys.argv) < 2):
		print 'usage error: sanders_corpora_extractor.py'
		print '-jM (For a json of all sentiments)'
		print '-jS (For separate jsons for pos, neg, and neu)'
		print '-txtM (For a text file of all sentiments)' 
		print '-txtS (For separate text files for pos, neg, and neu)'
		sys.exit(1)
		
	index =	build_index()
	dict_list = build_dict(index)
	output_file(dict_list,sys.argv[1])
	
if __name__ == '__main__':
	main()

	

