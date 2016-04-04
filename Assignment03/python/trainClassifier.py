# -*- coding: utf-8 -*-
import os, os.path
import sys, json
sys.path.append('/Users/rickardbergeling/GitHub/CS4242-Social-Media-Computing/Assignment03/python/libsvm-master/python')
import helper as helperClass
import reader, dictionary
import svm
import pickle
from svmutil import *
from pprint import pprint

helper = helperClass.Helper("data/stopwords.txt")

path_to_training_file = "data/Train/fromAssignment01.csv"
path_to_tweets = "data/Train/Tweets"
output_file = "data/Train/fromAssignment01Concatenated.csv"

print "Concatenating tweets into CSV file..."
reader.concatenateCSV(path_to_training_file, path_to_tweets, output_file)

# Requires delimiter ;

# path_to_training_data = "data/Train/databaseOutput.csv" 

path_to_training_data = output_file

print "Converting CSV into array..."
# Read training data stored in specified CSV file.
data = reader.CSVtoArrays(path_to_training_data, containsHeaders=True)
# data = reader.CSVtoArrays("data/Train/databaseOutput.csv", containsHeaders=True, delimiter=";")
rawTweets = data["text"]
rawLabels = data["sentiment"]

print "Translating labels..."
# Convert labels to numbers
labels = []
for l in rawLabels:
	labels.append(dictionary.translateSentiment(l))

print "Cleaning tweets..."
# Clean all the tweets, including stopword removal, stemming and custom feature removal
tweets = []
words = set()
for t in rawTweets:
	cleanedTweet = helper.clean(t)
	tweets.append(cleanedTweet)
	words = words.union(helper.extractWords(cleanedTweet))

# Update the helper feature list to all words found amongst the tweets
helper.setFeatureList(sorted(words))
pickle.dump(sorted(words), open("featureList.pkl", "wb"))

print "Generating feature vectors..."
# Generate feature vectors for each one of the tweets
featureVectors = []
for t in tweets:
	featureVectors.append(helper.getFeatureVector(t))

# Add a feature vector with all zeros which is classified as irrelevant
featureVectors.append([0]*len(featureVectors[0]))
labels.append(dictionary.translateSentiment("irrelevant"))

print "Training model..."
# Prepare SVM parameters
params = svm_parameter()
params.C = 10
params.kernel_type = LINEAR

# Prepare SVM problem
problem = svm_problem(labels, featureVectors)

# Train SVM Classifier
model = svm_train(problem, params)

print "Saving model..."
# Save trained model
svm_save_model('tweetClassifier.model', model)

print "Done!"