import os
import json
import pprint
import datetime
from sets import Set
from datetime import timedelta
import os.path


import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


folder = "tweet_data"
filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", \
"tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]

def extract_features_by_hour(tagID = 1):

	total_followers_count = 0.0
	total_retweets_count = 0.0
	total_tweets_count = 0.0
	total_hour_expand = 0.0
	total_user_ids = Set([])

	start_date = datetime.datetime(2015,03,28)
	end_date = datetime.datetime.fromtimestamp(datetime.MINYEAR)


	""" construct a hashmap to store the timestamp """
	d = {}
	user_dicts = {}
	""" read necessary data from file """
	fo = os.path.join(folder, filenames[tagID])

	with open(fo) as json_data:
		for json_line in json_data:


			tweet = json.loads(json_line)
			retweets = tweet["metrics"]["citations"]["data"][0]["citations"]
			user_id = tweet["tweet"]["user"]["id"]
			followers = tweet["author"]["followers"]
			
			date = tweet["firstpost_date"]
			date = datetime.datetime.fromtimestamp(date)
			time_key = datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0)
			time_key = unicode(time_key)

			if time_key not in d:
				d[time_key] = {'tweets_count':0, 'retweets_count':0, 'followers_count':0, 'max_followers':0, 'time':-1}
				user_dicts[time_key] = Set([])
			
			d[time_key]['tweets_count'] += 1
			d[time_key]['retweets_count'] += retweets
			if user_id not in user_dicts[time_key]:
				user_dicts[time_key].add(user_id)
				d[time_key]['followers_count'] += followers
				if followers > d[time_key]['max_followers']:
					d[time_key]['max_followers'] = followers
			d[time_key]['time'] = date.hour


			""" 
			for stats, problem 1.1
			"""
			total_tweets_count += 1
			total_retweets_count += retweets
			if user_id not in total_user_ids:
				total_user_ids.add(user_id)
				total_followers_count += followers
			if date < start_date:
				start_date = date
			if date > end_date:
				end_date = date

			
	total_hour_expand = int((end_date - start_date).total_seconds()/3600 + 0.5)
	stats_list = {'total_tweets_count':total_tweets_count, 'total_hour_expand':total_hour_expand, \
	'total_user_num':len(total_user_ids), 'total_retweets_count':total_retweets_count, \
	'total_followers_count':total_followers_count}
	
	for key in d:
		print key, 'values', d[key]

	with open(filenames[tagID]+'.json', 'wb') as fp:
		json.dump(d, fp)

	with open(filenames[tagID]+'stats.json', 'wb') as fp:
		json.dump(stats_list, fp)


def load_features_by_hour(tagID = 1):
	features_dict = {}
	fo = filenames[tagID] + ".json"

	if not os.path.exists(fo):
		print "file does not exist yet, creating it now..."
		extract_features_by_hour(tagID)

	with open(fo, 'rb') as json_data:
		for json_item in json_data:
			features_dict = json.loads(json_item)

	d = {}
	for key in features_dict:
		cur_hour = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
		value = features_dict[key]
		d[cur_hour] = value
		#print cur_hour, value
	return d

if __name__ == "__main__":

	#extract_features_by_hour(tagID = 2)
	for i in range(6):
		extract_features_by_hour(tagID = i)
		#features_dict = load_features_by_hour(tagID = id)
	

