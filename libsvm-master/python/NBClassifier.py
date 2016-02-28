import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re
import csv
import helper

class NBClassifier:
    __classifier = None
    __featureList = []
    __helper = None

    def __init__(self):
        self.__helper = helper.Helper()

    # def getClassifier(self):
    #     return self.__classifier

    def processTweet(self, tweet):
        tweet = self.__helper.clean(tweet)
        return tweet

    # def getFeatureVector(self, tweet):
    def getWordsInTweet(self, tweet):
        # Cleans the tweet and returns its words in an array
        return self.__helper.getNBFeatureVector(tweet)

    def getFeaturesFromWords(self, words):
        return self.__helper.getNBFeatures(words)

    def getFeaturesFromTweet(self, tweet):
        return self.__helper.getNBFeatures(self.__helper.getNBFeatureVector(tweet))

    def train(self, tweets):
        print "Getting feature list..."
        self.__helper.getFeatureList(tweets)

        print "Extracting features for each tweet in training set..."
        tweetTuples = []
        for i in range(1, len(tweets)-1):
            tweet = self.processTweet(tweets[i][0])
            sentiment = tweets[i][1]

            featureVector = self.getWordsInTweet(tweet) 
            self.__featureList.extend(featureVector)

            tweetTuples.append((featureVector, sentiment))

        print "Creating lazymap training set..."
        training_set = nltk.classify.util.apply_features(self.getFeaturesFromWords, tweetTuples)

        print "Training Naive Bayes classifier..."
        self.__classifier = nltk.NaiveBayesClassifier.train(training_set)

        self.__classifier.show_most_informative_features(20)


    def classify_tweet(self, tweet):
        return self.__classifier.classify(self.getFeaturesFromTweet(tweet))

    def classifyDataset(self, tweets, outfile):
        o = open(outfile, 'w')
        headers = ["Tweet", "Correct Sentiment", "Predicted Sentiment"]
        writer = csv.DictWriter(o, fieldnames=headers)
        writer.writeheader()

        tweet_features = []
        for i in range(0, len(tweets)-1):
            tweet_features.append(self.getFeaturesFromTweet(tweets[i][0]))

        sentiments = self.__classifier.classify_many(tweet_features)

        for i in range(0, len(tweets)-1):
            tweet = tweets[i][0]
            correct_sentiment = tweets[i][1]
            # predicted_sentiment = self.classify_tweet(tweet)
            writer.writerow({
                headers[0]: tweet, 
                headers[1]: correct_sentiment,
                headers[2]: sentiments[i]})
        o.close()