import svm
from svmutil import *
import pickle
import helper, reader

class SVMClassifier:
	def __init__(self):
		self.classifier = None
		self.helper = helper.Helper()
		self.model = None

	def classify(self, tweets, outfile):
		labels = []
		features = []
		for tweet in tweets:
			labels.append(self.helper.translateLabel(tweet[1]))
			features.append(self.helper.getSVMFeatureVector(tweet[0]))
		p_labs, p_acc, p_vals = svm_predict(labels, features, self.model)
		self.helper.saveSVMOutput(outfile, p_labs, tweets, p_acc, p_vals)

	def train(self, tweets):
		params = svm_parameter()
		params.C = 1
		params.kernel_type = LINEAR
		labels = []
		tweetFeatures = []
		for tweet in tweets:
			labels.append(self.helper.translateLabel(tweet[1]))
			tweetFeatures.append(self.helper.getSVMFeatureVector(tweet[0]))
		problem = svm_problem(labels, tweetFeatures)
		self.model = svm_train(problem, params)

	def cleanTweet(self, tweet):
		return self.helper.clean(tweet)

	def prepareHelper(self, tweets):
		self.helper.createLabelDictionary(tweets)
		self.helper.getFeatureList(tweets)

print "Preparing data..."
# Append the tweets to the CSV file
reader.appendTweets('data/training.csv', 'data/output/training-with-tweets.csv')

# Remove ambiguous information
tweets = reader.readTweets('data/output/training-with-tweets.csv', 'data/output/training-trimmed.csv')

print "Instantiating classifier..."
# Instantiate classifier
svm_c = SVMClassifier()
svm_c.prepareHelper(tweets)

print "Training classifier..."
# Train classifier
svm_c.train(tweets)

print "Preparing test data..."
# Prepare testing data by appending tweets to the CSV file
reader.appendTweets('data/testing.csv', 'data/output/testing-with-tweets.csv')
# Get the data from the test file and remove ambiguous information
testTweets = reader.readTweets('data/output/testing-with-tweets.csv', 'data/output/testing-trimmed.csv')

print "Classifying test data..."
# Run the classifier on the test data
svm_c.classify(testTweets, 'data/output/SVMResult.csv')

print "Getting stats..."

print "\n"
print "------------ SVM STATS ------------"
reader.getStats("data/output/SVMResult.csv")
print "\n"

print "Done!"