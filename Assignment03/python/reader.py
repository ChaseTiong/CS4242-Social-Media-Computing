# -*- coding: utf-8 -*-
import csv
import json
import sys
from pprint import pprint

def CSVtoArrays(path_to_csv, containsHeaders=False, delimiter=","):
	toBeReturned = {}

	f = open(path_to_csv, 'rb')
	reader = csv.reader(f, delimiter=delimiter)

	if(containsHeaders):
		headers = reader.next()
	else:
		headers = []
		for i in range(0, len(reader.next())):
			headers.append(i)
		f.seek(0)
		reader = csv.reader(f, delimiter=delimiter)

	for h in headers:
		toBeReturned[h] = []

	for row in reader:
		for h, v in zip(headers, row):
			toBeReturned[h].append(v)
	# pprint(toBeReturned)
	return toBeReturned

def concatenateCSV(path_to_training_file, path_to_tweets, output_file):
	f = open(path_to_training_file, "r").read().split("\n")
	tweets = []
	for i in range(1, len(f)-1):
	# for i in range(1, 5):
		tweet = {}
		[topic, sentiment, twitterID] = f[i].split(",")
		twitterID = twitterID.strip('"')
		tweet_data = json.load(open(path_to_tweets+"/"+twitterID+'.json'))

		tweet["id"] = tweet_data["id"]
		tweet["created_at"] = tweet_data["created_at"].encode("utf-8")
		tweet["lang"] = tweet_data["lang"].encode("utf-8")
		tweet["favourite_count"] = tweet_data["favorite_count"]
		tweet["retweet_count"] = tweet_data["retweet_count"]
		tweet["text"] = tweet_data["text"].encode("utf-8")
		tweet["sentiment"] = sentiment.strip('"')
		tweets.append(tweet)

	with open(output_file, 'w') as output:
	    fieldnames = ['id', 'created_at', 'lang', 'favourite_count', 'retweet_count', 'text', 'sentiment']
	    writer = csv.DictWriter(output, fieldnames=fieldnames)
	    writer.writeheader()
	    for tweet in tweets:
	    	writer.writerow({
	    		'id':tweet['id'],
	    		'created_at': tweet['created_at'],
	    		'lang': tweet['lang'],
	    		'favourite_count': tweet['favourite_count'],
	    		'retweet_count': tweet['retweet_count'],
	    		'text': tweet['text'],
	    		'sentiment': tweet['sentiment']
	    		})