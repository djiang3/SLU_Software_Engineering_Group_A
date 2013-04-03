# A program that will open a specified file and read from it. It also creates 4separate files for sorting of positive, negative, neutral, and trash tweets as well as a master JSON file of all of these three categories combined. All of these are in JSON.

import json
import os


def begin_sort(data):
    
    # Intialialize all of the lists required for the sort, including: master list, positive list, negative list, neutral list, trash list, save list, and the process counter.
    master_list = list()
    pos_list = list()
    neg_list = list()
    neu_list = list()
    irrel_list = list()
    save = list()
    p_cnt = 0

    print('z = Positive\nx = Negative\nc = Neutral\na = Trash\nq = Save and Quit\n[Enter] to skip the tweet.\n')

    # Traverse all dictionaries in the given json file, until q is entered.
    for dict in data:
        print dict['text']+'\n'

        confirm = raw_input()
        
        # Quit and save the manual sort process, including updating the manual_tweet json to represent existing tweets that have not been sorted yet.
        if(confirm == 'q'):
            break
    
        # 'z' to confirm that the tweet is positive
        elif(confirm == 'z'):
            dict['sentiment'] = 'positive'
            pos_list.append(dict)
            master_list.append(dict)

        # 'x' to confirm that the tweet is negative. 
        elif(confirm == 'x'):
            dict['sentiment'] = 'negative'
            neg_list.append(dict)
            master_list.append(dict)

        # 'c' to confirm that the tweet is neutral. 
        elif(confirm == 'c'):
            dict['sentiment'] = 'neutral'
            neu_list.append(dict)
            master_list.append(dict)

        # 'a' to confirm that the tweet is trash.
        elif(confirm == 'a'):
            dict['sentiment'] = 'irrelevant'
            irrel_list.append(dict)
            master_list.append(dict)
        p_cnt+=1

    try:
        os.makedirs('samples')
        print "Making samples folder..."
    except OSError:
        print "Entering samples folder..."
    fn = os.path.join(os.path.dirname(__file__), 'samples')
    os.chdir(fn)

    # Write all the tweets sorted so far into their respective files of pos, neg, neu, and trash.
    mas_out = json.dumps(master_list)
    pos_out = json.dumps(pos_list)
    neg_out = json.dumps(neg_list)
    neu_out = json.dumps(neu_list)
    irrel_out = json.dumps(irrel_list)

    master_sample = open('man_master.json','a')
    positive_sample = open('man_positive.json','a')
    negative_sample = open('man_negative.json','a')
    neutral_sample = open('man_neutral.json','a')
    irrelevant_sample = open('man_irrelevant.json','a')

    
    print "Files saving to samples directory..."
    master_sample.write(mas_out)
    positive_sample.write(pos_out)
    negative_sample.write(neg_out)
    neutral_sample.write(neu_out)
    irrelevant_sample.write(irrel_out)

    master_sample.close()
    positive_sample.close()
    negative_sample.close()
    neutral_sample.close()
    irrelevant_sample.close()
    print "All files saved successfully, saving progress..."
	            
	            
    # Index counter for determining the last tweet that has been processed.
    i_cnt = 0      
    # Left counter used for determining how many tweets are left.
    l_cnt = 0
    for dict in data:
        if(i_cnt >= p_cnt):
            save.append(dict)
            l_cnt+=1
        i_cnt += 1
	                
    # Update the manual_tweet json to represent tweets that have not yet been sorted.
    os.chdir('..')
    manual_json = open('manual_tweet.json', 'w+')
    save_out = json.dumps(save)
    manual_json.write(save_out)
    manual_json.close()
    
    print 'Progress saved.'
    
    print '\nNumber of tweets processed: ', p_cnt
    print 'Number of tweets remaining: ', l_cnt

def main():

    # Load the json file that will be examined.
    manual_json = open('manual_tweet.json','r')
    data = json.load(manual_json)
    
    # Begin the manual sort process.
    begin_sort(data)

if __name__ == '__main__':
    main()
