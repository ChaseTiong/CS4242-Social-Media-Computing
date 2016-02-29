import sys
import csv
import json

def getTweets(infile):
	f = open(infile, "r").read().split("\n")
	tweets = []
	for i in range(1, len(f)-1):
		tweet = {}
		[topic, sentiment, twitterID] = f[i].split(",")
		tweet["topic"] = topic.strip('"')
		tweet["sentiment"] = sentiment.strip('"')

		twitterID = twitterID.strip('"')
		tweet_data = json.load(open("data/tweets/"+twitterID+'.json'))
		
		tweet["text"] = tweet_data["text"]
		tweet["lang"] = json.dumps(tweet_data["lang"]).encode("utf-8").strip('"')

		tweets.append(tweet)
	return tweets

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
		if outfile:
			writer.writerow({
				headers[0]: classifierType, 
				headers[1]: sentiments[i], 
				headers[2]: tot, 
				headers[3]: true,
				headers[4]: false})
		Precision = float(true)/(true+false)*100.0
		Recall = float(true)/tot*100.0
		F1 = 2*(Precision*Recall)/(Precision+Recall)
		print "%-10.10s %10.2f%% %10.2f%% %10.2f%%" % (sentiments[i].capitalize(),Precision,Recall,F1)
	
	num_correct = stat_variables["num_correct"]
	num_false = stat_variables["num_false"]
	print "\n%-10.10s %10.2f%% %10i/%i" % ("Total Accuracy", float(num_correct)/float(num_correct+num_false)*100.0,	num_correct, num_correct+num_false)