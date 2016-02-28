import sys
import csv
import re

class Classifier:
	__posLex = None
	__negLex = None

	def __init__(self, path_to_posLex, path_to_negLex):
		positive_lexicon = set()
		with open(path_to_posLex) as pos:
			pos_words = pos.read().splitlines()
			for word in pos_words:
				positive_lexicon.add(word)
		negative_lexicon = set()
		with open(path_to_negLex) as neg:
			neg_words = neg.read().splitlines()
			for word in neg_words:
				negative_lexicon.add(word)
		self.__posLex = positive_lexicon
		self.__negLex = negative_lexicon

	def classify_tweet(self, tweet):
		num_pos = 0
		num_neg = 0
		tot_matches = 0
		tweet = re.sub('\.*', '', tweet)
		tweet = re.sub('\,*', '', tweet)
		tweet = re.sub('\!*', '', tweet)
		tweet = tweet.rstrip().lower().split(" ")

		# Iterate through words and count number of positive and negative words
		for word in tweet:
			if word in self.__posLex:
				num_pos += 1
				tot_matches += 1
			elif word in self.__negLex:
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

	def classifyDataset(self, tweets, outfile):
		o = open(outfile, 'w')
		headers = ["Tweet", "Correct Sentiment", "Predicted Sentiment"]
		writer = csv.DictWriter(o, fieldnames=headers)
		writer.writeheader()

		for i in range(0, len(tweets)-1):
			tweet = tweets[i][0]
			correct_sentiment = tweets[i][1]
			predicted_sentiment = self.classify_tweet(tweet)
			writer.writerow({
		        headers[0]: tweet, 
		        headers[1]: correct_sentiment,
		        headers[2]: predicted_sentiment})
		o.close()

# def classifyDataset(dataset, output, posLex, negLex):
# 	d = open(dataset, "r").read().split("\n")
# 	o = open(output, 'w')

# 	headers = ["Topic", "Sentiment", "Tweet"]

# 	writer = csv.DictWriter(o, fieldnames=headers)
# 	writer.writeheader()

# 	classification_stats = {}
# 	classification_stats["correctly_classified"] = 0
# 	classification_stats["incorrectly_classified"] = 0
# 	classification_stats["false_positives"] = 0
# 	classification_stats["false_negatives"] = 0
# 	classification_stats["false_neutrals"] = 0
# 	classification_stats["false_irrelevants"] = 0

# 	for i in range(1,len(d)-1):
# 		original_data = d[i].split(",")
# 		tweet = original_data[3]

# 		sentiment = classifyTweet(tweet, posLex, negLex)

# 		writer.writerow({
# 			headers[0]: original_data[0], 	#Topic
# 			headers[1]: sentiment, 			#Sentiment
# 			headers[2]: original_data[3] 	#Tweet
# 			})

# 		# Calculate incorrectly classified
# 		if sentiment == original_data[1]:
# 			classification_stats["correctly_classified"] += 1
# 		else:
# 			classification_stats["incorrectly_classified"] += 1
# 			if(sentiment == "positive"):
# 				classification_stats["false_positives"] += 1
# 			elif(sentiment == "negative"):
# 				classification_stats["false_negatives"] += 1
# 			elif(sentiment == "neutral"):
# 				classification_stats["false_neutrals"] += 1
# 			elif(sentiment == "irrelevant"):
# 				classification_stats["false_irrelevants"] += 1
# 			else:
# 				raise ValueError("Unknown sentiment: "+sentiment)

# 	printStats(classification_stats)

# def printStats(classification_stats):
# 	total_number_of_tweets = classification_stats["correctly_classified"] +classification_stats["incorrectly_classified"]
# 	print("------ Simple Classifier Stats ------")
# 	print("Correctly classified:   "+`classification_stats["correctly_classified"]`)
# 	print("incorrectly classified: "+`classification_stats["incorrectly_classified"]`)
# 	print("Accuracy:               "+`round(float(classification_stats["correctly_classified"])/total_number_of_tweets*100,2)`+"%")
# 	print("False positives:        "+`classification_stats["false_positives"]`)
# 	print("False negatives:        "+`classification_stats["false_negatives"]`)
# 	print("False neutrals:         "+`classification_stats["false_neutrals"]`)
# 	print("False irrelevants:      "+`classification_stats["false_irrelevants"]`)
# 	print("\nNote: Since the irrelevant tweets are the ones where no words were present in the dictionaries, these tweets were falsely classified due to limitations of said dictionaries.")
# 	print("The accuracy when not taking into account the tweets falsely classified as irrelevant would be "+
# 		`round(float(classification_stats["correctly_classified"])/(total_number_of_tweets - classification_stats["false_irrelevants"])*100,2)`
# 		+"%.")
# 	print("-------------------------------------")