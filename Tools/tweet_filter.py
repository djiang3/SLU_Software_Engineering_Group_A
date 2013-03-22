# A program that will open a specified file and read from it. It also creates 3 separate files for sorting of positive, negative, trash tweets, and useful trash tweets(used for a classifier separating tweets that are trash and tweets that are useful).

import os

# Specify the path containing the tweet data sample text.
os.chdir("/PATH")

# Opens the sample text.
openFile = open('sample_tweet.txt','r')

# Open/create the files for storing data.
posTweet_sample = open('posTweet_sample.txt','a')
negTweet_sample = open('negTweet_sample.txt','a')
trashTweet_sample = open('trashTweet_sample.txt','a')
useTrashTweet_sample = open('useTrashTweet_sample.txt','a')

posList = list()
negList = list()
trashList = list()
useTrashList = list()
data = list()

cnt = 0

print('z = Positive\nx = Negative\nc = Trash\na = Useful Trash\nq = Save and Quit\n[Enter] to skip the tweet.\n')
for line in openFile:
  confirm = raw_input(line)
  if(confirm == 'q'):
    print '\nNumber of tweets processed: ',cnt
    cnt = 0
    data.append(line)
    for line in openFile:
      data.append(line)
      cnt+=1
      print 'Number of tweets remaining: ',cnt
      break
  elif(confirm == 'z'):
    posList.append(line)
  elif(confirm == 'x'):
    negList.append(line)
  elif(confirm == 'c'):
    trashList.append(line)
  elif(confirm == 'a'):
    useTrashList.append(line)
  cnt+=1
	
dataOut = ''.join(data)
posOut = ''.join(posList)
negOut = ''.join(negList)
trashOut = ''.join(trashList)
useTrashOut = ''.join(useTrashList)

if(len(posList) > 0):
  posTweet_sample.write(str(posOut))
if(len(negList) > 0):
  negTweet_sample.write(str(negOut))
if(len(trashList) > 0):
  trashTweet_sample.write(str(trashOut))
if(len(useTrashList) > 0):
  useTrashTweet_sample.write(str(useTrashOut))

openFile = open('sample_tweet.txt','r+')
openFile.write(str(dataOut))

# Cleanly close all of the files
posTweet_sample.close() 
negTweet_sample.close()
trashTweet_sample.close()
useTrashTweet_sample.close()
openFile.close()

