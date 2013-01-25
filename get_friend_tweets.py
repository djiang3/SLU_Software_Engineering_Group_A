import twitter

friendIDs = []
friendNames = []
timelines = []
tweets = []
allFriends = []

#will need to hide these eventually. ideas welcome!
#possibly just hidden dir if eventually daemon?
CONSUMER_KEY = 'XldG48dh2WzV4XMvhDaA'
CONSUMER_SECRET = '1c429FQnjAzaFwOhzwJC3h4qEi4YwR7UhW2ickl5kc'
ACCESS_TOKEN_KEY = '1112662302-lEnMQewEG47MJw9yWN0lMOQdk5DHaqEU7FgDM2V'
ACCESS_TOKEN_SECRET = 'LwlVCS5fwqVmkvlwqQiB5Z7PepnITzq9ynUr8NPkA'

ID_INDEX = 'ids'
	
class Friend:
	def __init__(self, id, name, tweets, weight=1):
		self.id = id
		self.name = name
		self.weightRating = weight
		self.tweets = tweets
		#tweet time accessed through Status object

#load api
def initializeAPI():
	try:
		api = twitter.Api(consumer_key=CONSUMER_KEY, \
				consumer_secret=CONSUMER_SECRET, \
				access_token_key=ACCESS_TOKEN_KEY, \
				access_token_secret=ACCESS_TOKEN_SECRET)
		return api
	except twitter.TwitterError:
		print "API could not be loaded"

#get friend ids from app account
def main():
	api = initializeAPI()

	#throws json error on fail
	friendIDs = api.GetFriendIDs()

	#throws json error on fail
	friendNames = api.GetFriends()

	for id in friendIDs[ID_INDEX]:
		timelines.append(api.GetFriendsTimeline(id))

	for i in range(len(friendIDs[ID_INDEX])):
		friend = Friend(friendIDs[ID_INDEX][i], friendNames[i].name, timelines[i])
		allFriends.append(friend)

	for f in allFriends:
		print "%s:" % (f.name)
		for t in f.tweets:
			print(t.text)
		print ("\n")

if __name__ == '__main__':
	main()
