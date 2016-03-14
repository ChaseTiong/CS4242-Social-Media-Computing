# NBClassifier.py
import nltk
from nltk import pos_tag
# from nltk.tokenize import word_tokenize
import re
import csv
import helper

class NBClassifier:
    __classifier = None
    __featureList = []
    __helper = None

    def __init__(self):
        self.__helper = helper.Helper()

    def getFeatureVectorFromTweet(self, tweet):
        return self.__helper.getFeatureVectorFromTweet(tweet)

    def train(self, tweets):
        print "Getting NB Feature List..."
        # Get the feature list which will be used to create the feature vectors. The True is for enabling stopwords. 
        self.__helper.getNBFeatureList(tweets, True)

        print "Creating lazymap training set..."
        tweetTuples = []
        for i in range(1, len(tweets)-1):
            tweetTuples.append((tweets[i], tweets[i]["sentiment"]))
        training_set = nltk.classify.util.apply_features(self.getFeatureVectorFromTweet, tweetTuples)

        print "Training Naive Bayes classifier..."
        self.__classifier = nltk.NaiveBayesClassifier.train(training_set)
        self.__classifier.show_most_informative_features(20)

    def classify_tweet(self, tweet):
        return self.__classifier.classify(self.getFeatureVectorFromTweet(tweet))

    def classifyDataset(self, tweets, outfile):
        o = open(outfile, 'w')
        headers = ["Tweet", "Correct Sentiment", "Predicted Sentiment"]
        writer = csv.DictWriter(o, fieldnames=headers)
        writer.writeheader()

        print "Applying feature algorithm to all tweets in testing set..."
        tweet_features = []
        for i in range(0, len(tweets)):
            tweet_features.append(self.getFeatureVectorFromTweet(tweets[i]))

        print "Classifying tweets..."
        sentiments = self.__classifier.classify_many(tweet_features)

        for i in range(0, len(tweets)):
            tweet = self.__helper.clean(tweets[i]["text"]).encode('utf-8')
            correct_sentiment = tweets[i]["sentiment"]
            writer.writerow({
                headers[0]: tweet, 
                headers[1]: correct_sentiment,
                headers[2]: sentiments[i]})
        o.close()