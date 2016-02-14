import sys
import csv
import re

def classifyDataset(dataset, output, posLex, negLex):
	d = open(dataset, "r").read().split("\n")
	o = open(output, 'w')

	headers = ["Topic", "Sentiment", "Tweet"]

	writer = csv.DictWriter(o, fieldnames=headers)
	writer.writeheader()

	classification_stats = {}
	classification_stats["correctly_classified"] = 0
	classification_stats["incorrectly_classified"] = 0
	classification_stats["false_positives"] = 0
	classification_stats["false_negatives"] = 0
	classification_stats["false_neutrals"] = 0
	classification_stats["false_irrelevants"] = 0

	for i in range(1,len(d)-1):
		original_data = d[i].split(",")
		tweet = original_data[3]

		sentiment = classifyTweet(tweet, posLex, negLex)

		writer.writerow({headers[0]: original_data[0], headers[1]: sentiment, headers[2]: original_data[3]})

		# Calculate incorrectly classified
		if sentiment == original_data[1]:
			classification_stats["correctly_classified"] += 1
		else:
			classification_stats["incorrectly_classified"] += 1
			if(sentiment == "positive"):
				classification_stats["false_positives"] += 1
			elif(sentiment == "negative"):
				classification_stats["false_negatives"] += 1
			elif(sentiment == "neutral"):
				classification_stats["false_neutrals"] += 1
			elif(sentiment == "irrelevant"):
				classification_stats["false_irrelevants"] += 1
			else:
				raise ValueError("Unknown sentiment")

	printStats(classification_stats)

def classifyTweet(tweet, posLex, negLex):
	num_pos = 0
	num_neg = 0
	tot_matches = 0
	tweet = re.sub('\.*', '', tweet)
	tweet = re.sub('\,*', '', tweet)
	tweet = re.sub('\!*', '', tweet)
	tweet = tweet.rstrip().lower().split(" ")

	# Iterate through words and count number of positive and negative words
	for word in tweet:
		if word in posLex:
			num_pos += 1
			tot_matches += 1
		elif word in negLex:
			num_neg += 1
			tot_matches += 1

	
	if tot_matches == 0: # If no word has been matched with the lexicon, the tweet is considered irrelevant
		sentiment = "irrelevant"
	else:
		if num_pos == num_neg:
			sentiment = "neutral"
		elif num_neg > num_pos:
			sentiment = "negative"
		elif num_neg < num_pos:
			sentiment = "positive"
		else:
			raise ValueError('Tweet not classified')
	return sentiment

def printStats(classification_stats):
	print("------ Simple Classifier Stats ------")
	print("Accuracy:          "+`round(float(classification_stats["correctly_classified"])/(classification_stats["correctly_classified"]+classification_stats["incorrectly_classified"]),2)`+"%")
	print("False positives:   "+`classification_stats["false_positives"]`)
	print("False negatives:   "+`classification_stats["false_negatives"]`)
	print("False neutrals:    "+`classification_stats["false_neutrals"]`)
	print("False irrelevants: "+`classification_stats["false_irrelevants"]`)
	print("-------------------------------------")