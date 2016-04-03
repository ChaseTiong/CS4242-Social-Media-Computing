# -*- coding: utf-8 -*-
import os, os.path
import sys
sys.path.append('/Users/rickardbergeling/GitHub/CS4242-Social-Media-Computing/Assignment02/libsvm-master/python')
import reader
import helper as helperClass
import pickle
from pprint import pprint
import time
import svm
from svmutil import *
import re
import json

def main():
	extractData = False
	extractTestingData = False
	helper = helperClass.Helper()
	path_to_training_directory = "data/Train"
	# path_to_testing_directory = "data/Test"
	path_to_testing_directory = "multi-view-online-testing"
	path_to_training_labels = "data/Train/GroundTruth/groundTruth.txt"
	path_to_testing_labels = "multi-view-online-testing/GroundTruth/groundTruth.txt"
	# path_to_testing_labels = "data/Test/GroundTruth/groundTruth.txt"

	if(extractData):
		truths = open(path_to_training_labels, "r").read().split("\n")

		print "Extracting user training data..."

		userData = []
		for i in range(1, len(truths)):
			userData.append(reader.readData(i, helper, path_to_training_directory))
			sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i)/(len(truths)-1)*100), i, len(truths)-1))
			sys.stdout.flush()
		print "\r"

		pickle.dump(userData, open("userData.pkl", "wb"))
	else:
		userData = pickle.load(open("userData.pkl", "rb"))


	allWords = set()
	userWords = {}
	
	print "Extracting unique words from user data..."
	for i in range(0, len(userData)):
		userWords[i] = helper.getUserWords(userData[i])
		allWords = allWords.union(userWords[i])
		sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i+1)/len(userData)*100), i+1, len(userData)))
		sys.stdout.flush()

	print "\n"+str(len(allWords))+" unique words found.\n"
	# print allWords
	helper.setFeatureList(sorted(allWords))
	
	with open('allWords.txt', 'w') as outfile:
		json.dump(sorted(allWords), outfile)

	featureVectors = []
	print "Generating feature vectors..."

	for i in range(0, len(userData)):
		featureVectors.append(helper.getFeatureVector(userWords[i]))
		sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i+1)/len(userData)*100), i+1, len(userData)))
		sys.stdout.flush()

	print "\r"
	labelVectors = helper.getLabelVectors(path_to_training_labels)

	print "Training SVM models..."
	params = svm_parameter()
	params.C = 10
	params.kernel_type = LINEAR

	# labels = labelVectors[0]
	models = {}
	for i in range(0, len(labelVectors)):
		problem = svm_problem(labelVectors[i], featureVectors)
		models[i] = svm_train(problem, params)

	# problem = svm_problem(labels, featureVectors)
	# model = svm_train(problem, params)

	if(extractTestingData):
		truths = open(path_to_testing_labels , "r").read().split("\n")

		print "Extracting user testing data..."
		userIdPattern = re.compile("U(\d*?)gnd.txt")
		userIDs = userIdPattern.findall(" ".join(os.listdir(path_to_testing_directory+"/GroundTruth")))
		userIDs = map(int, userIDs)

		userData = []
		for i in range(0, len(userIDs)):
			userData.append(reader.readData(userIDs[i], helper, path_to_testing_directory))
			sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i+1)/(len(userIDs))*100), i+1, len(userIDs)))
			sys.stdout.flush()
		print "\r"

		pickle.dump(userData, open("userTestingData.pkl", "wb"))
	else:
		userData = pickle.load(open("userTestingData.pkl", "rb"))


	print "Generating feature vectors..."
	featureVectors = []
	for i in range(0, len(userData)):
		featureVectors.append(helper.getFeatureVector(helper.getUserWords(userData[i])))
		sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i+1)/len(userData)*100), i+1, len(userData)))
		sys.stdout.flush()

	print "\r"
	labelVectors = helper.getLabelVectors(path_to_testing_labels)
	
	avgAcc = 0.0
	labelContainer = []
	print "Classifying dataset..."
	for i in range(0, len(models)):
		p_labels, p_accs, p_vals = svm_predict(labelVectors[i], featureVectors, models[i])
		labelContainer.append(p_labels)
		avgAcc = avgAcc+p_accs[0]

	avgAcc = avgAcc/(len(models))
	print "Average accuracy: "+str(avgAcc)+"%"

	reader.saveOutput(labelContainer, 'data/outputLabels.csv')
	pickle.dump(labelContainer, open("outputLabels.pkl", "wb"))
	reader.getSaK()
	# p_labels, p_accs, p_vals = svm_predict(labelVectors[0], featureVectors, model)


main()




