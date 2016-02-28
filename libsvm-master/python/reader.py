import sys
import csv
import json

def appendTweets(infile, outfile):
	f = open(infile, "r").read().split("\n")
	o = open(outfile, 'w')

	headers = f[0].split(",")
	headers.append("Tweet")
	writer = csv.DictWriter(o, fieldnames=headers)
	writer.writeheader()

	for i in range(1,len(f)-1):
		original_data = f[i].split(",")
		tweet_data_file = open("data/tweets/"+original_data[2].strip('"')+'.json')
		tweet_data = json.load(tweet_data_file)
		tweet_data_file.close()
		tweet_text = json.dumps(tweet_data["text"]).encode("utf-8")
		writer.writerow({headers[0]: original_data[0].strip('"'), headers[1]: original_data[1].strip('"'), headers[2]: original_data[2].strip('"'), headers[3]: tweet_text.strip('"')})
	o.close()

def readTweets(infile, outfile):
	f = open(infile, "r").read().split("\n")
	o = open(outfile, 'w')
	reader = csv.reader( f, delimiter=',', quotechar='"', escapechar='\\' )
	writer = csv.writer(o)
	tweets = list(reader)
	
	# Remove header row
	del tweets[0]
	# Remove last item because it is empty
	del tweets[len(tweets)-1]
	for i in range(0, len(tweets)):
		# Remove topic row
		del tweets[i][0]
		
		# Remove twitter ID row
		del tweets[i][1]

		# Create tuple
		tweets[i] = (tweets[i][1], tweets[i][0])
		writer.writerow([tweets[i][0], tweets[i][1]])
	return tweets

def getStats(infile):
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

	print "%0-10s %10s %10s" % ("Topic", "Accuracy", "Ratio")
	for i in range(0, len(sentiments)):
		true = stat_variables["true_"+sentiments[i]]
		false = stat_variables["false_"+sentiments[i]]
		tot = stat_variables["num_"+sentiments[i]]
		print "%-10.10s %8.2f%% %8i/%i" % (sentiments[i].capitalize(),float(true)/float(tot)*100.0 ,true, tot)
	
	num_correct = stat_variables["num_correct"]
	num_false = stat_variables["num_false"]
	print "%-10.10s %8.2f%% %8i/%i" % ("Total", float(num_correct)/float(num_correct+num_false)*100.0, num_correct, num_correct+num_false)






