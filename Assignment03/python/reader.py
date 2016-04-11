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
	    	if(tweet["lang"] == ("en") or True):
		    	writer.writerow({
		    		'id':tweet['id'],
		    		'created_at': tweet['created_at'],
		    		'lang': tweet['lang'],
		    		'favourite_count': tweet['favourite_count'],
		    		'retweet_count': tweet['retweet_count'],
		    		'text': tweet['text'],
		    		'sentiment': tweet['sentiment']
		    		})

def getStats(infile, outfile = False, classifierType = None):
	f = open(infile, "r").read().split("\n")
	reader = csv.reader( f, delimiter=',', quotechar='"', escapechar='\\' )
	data = list(reader)
	sentiments = []
	for i in range(1, len(data)-1):
		if data[i][1] not in sentiments:
			sentiments.append(data[i][1])
	sentiments = sorted(sentiments)

	stat_variables = {}
	for i in range(0, len(sentiments)):
		stat_variables["true_"+sentiments[i]] = 0
		stat_variables["false_"+sentiments[i]] = 0
		stat_variables["num_"+sentiments[i]] = 0
	stat_variables["num_correct"] = 0
	stat_variables["num_false"] = 0
	
	if outfile:
		o = open(outfile, 'w')
		headers = ["Classifier", "Sentiment", "Total", "True", "False"]
		writer = csv.DictWriter(o, fieldnames=headers)

	for i in range(1, len(data)-1):
		correct_sentiment = data[i][1]
		predicted_sentiment = data[i][2]
		stat_variables["num_"+correct_sentiment] += 1
		if predicted_sentiment != correct_sentiment:
			stat_variables["false_"+predicted_sentiment] += 1
			stat_variables["num_false"] += 1
		else:
			stat_variables["true_"+correct_sentiment] += 1
			stat_variables["num_correct"] += 1

	print "%0-10s %11s %11s %10s" % ("Topic", "Precision", "Recall", "F1")

	for i in range(0, len(sentiments)):
		true = stat_variables["true_"+sentiments[i]]
		false = stat_variables["false_"+sentiments[i]]
		tot = stat_variables["num_"+sentiments[i]]

		Precision = float(true)/(true+false)*100.0
		Recall = float(true)/tot*100.0
		F1 = 2*(Precision*Recall)/(Precision+Recall)
		print "%-10.10s %10.2f%% %10.2f%% %10.2f%%" % (sentiments[i].capitalize(),Precision,Recall,F1)
	
	num_correct = stat_variables["num_correct"]
	num_false = stat_variables["num_false"]
	print "\n%-10.10s %10.2f%% %10i/%i" % ("Total Accuracy", float(num_correct)/float(num_correct+num_false)*100.0,	num_correct, num_correct+num_false)

def saveSVMOutput(outfile, tweets, predictedLabels, correctLabels):
	print "Saving outfile to "+outfile+"..."
	o = open(outfile, 'w')
	headers = ["Tweet", "Correct Sentiment", "Predicted Sentiment"]
	writer = csv.DictWriter(o, fieldnames=headers)
	writer.writeheader()

	for i in range(0, len(predictedLabels)):
		correct_label = correctLabels[i]
		predicted_label = predictedLabels[i]
		tweetText = tweets[i]
		writer.writerow({
			headers[0]: tweetText, 
			headers[1]: correct_label,
			headers[2]: predicted_label})
	o.close()