# A program that will open a specified file and read from it. It also creates 3separate files for sorting of positive, negative, trash tweets, and useful trash tweets(used for a classifier separating tweets that are trash and tweets that are useful).  

import json
import codecs
def sort(data):
    
    master_list = list()
    pos_list = list()
    neg_list = list()
    neu_list = list()
    trash_list = list()
    save = list()
    tweet_cnt = 0

    print('z = Positive\nx = Negative\nc = Neutral\na = Trash\nq = Save and Quit\n[Enter] to skip the tweet.\n')

    for dict in data:
        print dict['text']+'\n'

        confirm = raw_input()

        if(confirm == 'q'):
            print '\nNumber of tweets processed: ',tweet_cnt
            cnt = 0

            mas_out = json.dumps(master_list)
            pos_out = json.dumps(pos_list)
            neg_out = json.dumps(neg_list)
            neu_out = json.dumps(neu_list)

            master_sample = open('man_master.json','a')
            positive_sample = open('man_positive.json','a')
            negative_sample = open('man_negative.json','a')
            neutral_sample = open('man_neutral.json','a')

            master_sample.write(mas_out+"\n")
            positive_sample.write(pos_out+"\n")
            negative_sample.write(neg_out+"\n")
            neutral_sample.write(neu_out+"\n")
            
            master_sample.close()
            positive_sample.close()
            negative_sample.close()
            neutral_sample.close()

            save.append(dict)
            for dict in data:
                save.append(dict)
                cnt+=1
            print 'Number of tweets remaining: ',cnt
            break
    

        elif(confirm == 'z'):
            dict['sentiment'] = 'positive'
            pos_list.append(dict)
            master_list.append(dict)

        elif(confirm == 'x'):
            dict['sentiment'] = 'negative'
            neg_list.append(dict)
            master_list.append(dict)

        elif(confirm == 'c'):
            dict['sentiment'] = 'neutral'
            neu_list.append(dict)
            master_list.append(dict)

        elif(confirm == 'a'):
            trash_list.append(dict)
            master_list.append(dict)
        tweet_cnt+=1
    return save
def main():
    
    manual_json = open('manual_tweet.json','r')
    data = json.load(manual_json)
    
    manual_json = open('manual_tweet.json', 'r+')

    save = sort(data)
    save_out = json.dumps(save)
    manual_json.write(save_out)

    manual_json.close()

if __name__ == '__main__':
    main()
