# SVMClassifier.py
import svm
from svmutil import *
import pickle
import helper, reader

class SVMClassifier:
	__helper = None
	__model = None

	def __init__(self):
		self.__helper = helper.Helper()

	def prepareHelper(self, tweets):
		self.__helper.createDictionaries(tweets)
		self.__helper.getFeatureList(tweets)

	def train(self, tweets):
		params = svm_parameter()
		params.C = 1
		params.kernel_type = LINEAR
		labels = []
		tweetFeatures = []
		for tweet in tweets:
			labels.append(self.__helper.translateLabel(tweet["sentiment"]))
			tweetFeatures.append(self.__helper.getSVMFeatureVector(tweet))
		problem = svm_problem(labels, tweetFeatures)
		self.__model = svm_train(problem, params)

	def classify(self, tweets, outfile):
		labels = []
		features = []

		for tweet in tweets:
			labels.append(self.__helper.translateLabel(tweet["sentiment"]))
			features.append(self.__helper.getSVMFeatureVector(tweet))

		p_labs, p_acc, p_vals = svm_predict(labels, features, self.__model)
		self.__helper.saveSVMOutput(outfile, p_labs, tweets, p_acc, p_vals)