import nltk
import re
from nltk import pos_tag
from nltk.tokenize import TweetTokenizer
# from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

class Classifier:
	__word_features = []
	__classifier = None

	def __init__(self, word_features):
		self.__word_features = word_features

	def train(self, training_set):
		self.__classifier = nltk.NaiveBayesClassifier.train(training_set)
		self.__classifier.show_most_informative_features(32)

	def extract_features(self, tweet):
		tweet_words = set(tweet)
		features = {}
		for word in self.__word_features:
			features['contains(%s)' % word] = (word in tweet_words)
		return features

	def classify_tweet(self, tweet):
		stemmed_words = []
		for word in tweet.split():
			stemmed_words.append(stem(word))
		stemmed_tweet = " ".join(stemmed_words)
		return self.__classifier.classify(self.extract_features(stemmed_tweet))

def stem(word):
	return LancasterStemmer().stem(word)

def trim_training_data(path_to_data):
	trainingData = open(path_to_data, "r").read().split("\n")
	all_tweets = []

	# for i in range(1,len(trainingData)-1):

	for i in range(1,20):
		tweet_data = (trainingData[i].split(",")[3], trainingData[i].split(",")[1])
		all_tweets.append(tweet_data)

	tweets = []
	for (words, sentiment) in all_tweets:
		# words = re.sub('\.*', '', words) # Remove all dots
		# words = re.sub('\,*', '', words) # Remove all commas
		# words = re.sub('\!*', '', words) # Remove all exclamation marks
		# words = re.sub('\@\S*', '', words) # Remove all twitter mentions (@apple etc.)
		words_filtered = [stem(e.lower()) for e in words.split()]
		tweets.append((words_filtered, sentiment))
	    
	return tweets


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def trainClassifier(path_to_data):
	tweets = trim_training_data(path_to_data)
	word_features = get_word_features(get_words_in_tweets(tweets))
	classifier = Classifier(word_features)
	training_set = nltk.classify.apply_features(classifier.extract_features, tweets) 
	classifier.train(training_set)

	return classifier

def classifyDataset(classifier, dataset):
	testing_data = open(dataset, "r").read().split("\n")
	for i in range(1,20):
		print(testing_data[i].split(","))
		# print(classifier.classify_tweet())
