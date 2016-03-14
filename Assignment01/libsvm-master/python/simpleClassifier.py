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

		for i in range(0, len(tweets)):
			tweet = tweets[i]["text"].encode('utf-8')
			correct_sentiment = tweets[i]["sentiment"]
			predicted_sentiment = self.classify_tweet(tweet)
			writer.writerow({
		        headers[0]: tweet, 
		        headers[1]: correct_sentiment,
		        headers[2]: predicted_sentiment})
		o.close()