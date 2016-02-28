import svm
from svmutil import *
import pickle
import helper, reader

class SVMClassifier:
	__helper = None
	__model = None

	def __init__(self):
		# __classifier = None
		self.__helper = helper.Helper()
		self.__model = None

	def classify(self, tweets, outfile):
		labels = []
		features = []
		for tweet in tweets:
			labels.append(self.__helper.translateLabel(tweet[1]))
			features.append(self.__helper.getSVMFeatureVector(tweet[0]))
		p_labs, p_acc, p_vals = svm_predict(labels, features, self.__model)
		self.__helper.saveSVMOutput(outfile, p_labs, tweets, p_acc, p_vals)

	def train(self, tweets):
		params = svm_parameter()
		params.C = 1
		params.kernel_type = LINEAR
		labels = []
		tweetFeatures = []
		for tweet in tweets:
			labels.append(self.__helper.translateLabel(tweet[1]))
			tweetFeatures.append(self.__helper.getSVMFeatureVector(tweet[0]))
		problem = svm_problem(labels, tweetFeatures)
		self.__model = svm_train(problem, params)

	def cleanTweet(self, tweet):
		return self.__helper.clean(tweet)

	def prepareHelper(self, tweets):
		self.__helper.createLabelDictionary(tweets)
		self.__helper.getFeatureList(tweets)