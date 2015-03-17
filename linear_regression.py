import os
import json
import pprint
import datetime
from sets import Set
from datetime import timedelta
import sys


import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

from features_by_hour import load_features_by_hour

folder = "tweet_data"
filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", \
"tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]

def group_features_by_hour(tagID = 1):
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
	for key in d:
		print key, 'values', d[key]
	return d

def construct_matrix(d):
	""" 
		Construct X, y for regression 
		here y is the number of tweets for next hour
	"""
	start_time = min(d.keys()) 
	end_time = max(d.keys())	
	X = []
	y = []
	cur_hour = start_time
	while cur_hour < end_time:

		""" y value """
		tweets_count_next_hour = 0
		next_hour = cur_hour+timedelta(hours=1)
		if next_hour in d:
			tweets_count_next_hour = d[next_hour]['tweets_count']

		""" X values """
		if cur_hour in d:
			#item = d[cur_hour].values() + [tweets_count_next_hour]
			X.append(d[cur_hour].values())
			y.append([tweets_count_next_hour])
			#print item
		else:
			temp = {'tweets_count':0, 'retweets_count':0, 'followers_count':0, 'max_followers':0, 'time':cur_hour.hour}
			#item = temp.values() + [tweets_count_next_hour]
			X.append(temp.values())
			y.append([tweets_count_next_hour])
			#print item

		cur_hour = next_hour

	return X, y


if __name__ == "__main__":

	Xs = []
	ys = []
	for i in range(6):
		""" for each hashtag, get features"""
		d = load_features_by_hour(tagID = 0)
		X, y = construct_matrix(d)
		Xs = Xs + X
		ys = ys + y

	model = sm.OLS(ys, Xs)
	results = model.fit()
	print(results.summary())
	with open("linear_regression_result.txt", 'wb') as fp:
		print >>fp, results.summary()





