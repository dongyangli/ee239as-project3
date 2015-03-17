import os
import json
import pprint
import datetime
from sets import Set
import collections
from datetime import timedelta

from features_by_hour import load_features_by_hour

folder = "tweet_data"
filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", \
"tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]
hashtags = ["#gohawks", "#gopatriots", "#nfl", \
"#patriots", "#sb49", "#superbowl"]

def hashtag_stats(tagID = 1):

	followers_count = 0.0
	retweets_count = 0.0
	tweets_count = 0.0
	hours_count = 0.0

	start_date = datetime.datetime(2015,03,20)
	end_date = datetime.datetime.fromtimestamp(datetime.MINYEAR)

	user_ids = Set([])
	fo = os.path.join(folder, filenames[tagID])

	with open(fo, 'rb') as json_data:
		for json_line in json_data:

			tweet = json.loads(json_line)
			
			tweets_count += 1
			# for each tweet
			retweets = tweet["metrics"]["citations"]["data"][0]["citations"]
			retweets_count += retweets

			date = tweet["firstpost_date"]
			date = datetime.datetime.fromtimestamp(date)
			if date < start_date:
				start_date = date
			if date > end_date:
				end_date = date
				
			# for users and users' followers
			user_id = tweet["tweet"]["user"]["id"]
			followers = tweet["author"]["followers"]
			if user_id not in user_ids:
				user_ids.add(user_id)
				followers_count += followers

	print start_date.strftime('%Y-%m-%d %H:%M:%S')
	print end_date.strftime('%Y-%m-%d %H:%M:%S')
	hours_count = int((end_date - start_date).total_seconds()/3600 + 0.5)

	print "total number of hour is ", hours_count
	print "total number of users posting this hashtag is ", len(user_ids)
	print "total number of tweets containing this hashtag is ", tweets_count
	print "total number of retweets is ", retweets_count

	return tweets_count/hours_count, followers_count/len(user_ids), retweets_count/tweets_count



import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(tagID, d):


	""" construct a hashmap to store the timestamp 
	d = {}

	fo = os.path.join(folder, filenames[1])

	with open(fo) as json_data:
		for json_line in json_data:

			tweet = json.loads(json_line)

			date = tweet["firstpost_date"]
			date = datetime.datetime.fromtimestamp(date)
			time_key = datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0)
			if time_key not in d:
				d[time_key] = 1
			else:
				d[time_key] += 1

			#print "date", time_key
	"""			
	#sorted_d = collections.OrderedDict(sorted(d.items(), key=lambda t: t[0]))
	sorted_d = d
	start_time = min(sorted_d.keys()) 
	end_time = max(sorted_d.keys())

	tweets_per_hour = []

	cur = start_time
	while cur <= end_time:
		if cur in sorted_d:
			#tweets_per_hour[cur] = sorted_d[cur]
			tweets_per_hour.append(sorted_d[cur]["tweets_count"])
		else:
			#tweets_per_hour[cur] = 0
			tweets_per_hour.append(0)

		cur += timedelta(hours=1)



	#tweets_per_hour = collections.OrderedDict(sorted(tweets_per_hour.items(), key=lambda t: t[0]))
	#for key in tweets_per_hour:
		#print key, 'corresponds to ', tweets_per_hour[key]
	#print tweets_per_hour.values()
	#print tweets_per_hour
	plt.figure(figsize=(20, 8))
	plt.title("Number of Tweets in Hour for [" + hashtags[tagID] + "]")
	plt.ylabel("number of tweets")
	plt.xlabel("timeline")
	#plt.hist(tweets_per_hour, bins = range(max(tweets_per_hour)), histtype='bar')
	plt.bar(range(len(tweets_per_hour)), tweets_per_hour, width=1.5, color='b')
	plt.show()

if __name__ == "__main__":
	#print hashtag_stats()
	#plot_histogram()

	id1 = 2 # nfl
	d1 = load_features_by_hour(tagID = id1)
	plot_histogram(id1, d1)

	id2 = 5 # superbowl
	d2 = load_features_by_hour(tagID = id2)
	plot_histogram(id2, d2)




