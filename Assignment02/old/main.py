# -*- coding: utf-8 -*-
import os, os.path
import reader
import helper as helperClass
import pickle
from pprint import pprint
import sys
import time
import svm
from svmutil import *


def main():
	extractData = False
	helper = helperClass.Helper()
	path_to_training_directory = "data/Train"
	path_to_testing_directory = "data/Test"
	path_to_training_labels = "data/Train/GroundTruth/groundTruth.txt"

	if(extractData):
		truths = open(path_to_training_labels, "r").read().split("\n")

		print "Extracting user data..."

		userData = []
		for i in range(1, len(truths)):
			userData.append(reader.readData(i, helper, path_to_training_directory))
			sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i)/(len(truths)-1)*100), i, len(truths)-1))
			sys.stdout.flush()
		print "\r"

		pickle.dump(userData, open("userData.pkl", "wb"))
	else:
		userData = pickle.load(open("userData.pkl", "rb"))

	labelVectors = helper.getLabelVectors(path_to_training_labels)
	print str(len(labelVectors))+" label vectors created"

	allWords = set()
	userWords = {}
	
	print "Extracting unique words from user data..."
	for i in range(0, len(userData)):
		userWords[i] = helper.getUserWords(userData[i])
		allWords = allWords.union(userWords[i])
		sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i+1)/len(userData)*100), i+1, len(userData)))
		sys.stdout.flush()

	print "\n"+str(len(allWords))+" unique words found.\n"
	
	helper.setFeatureList(sorted(allWords))

	featureVectors = []
	print "Generating feature vectors..."

	for i in range(0, len(userData)):
		featureVectors.append(helper.getFeatureVector(userWords[i]))
		sys.stdout.write("\r%5.2f%% (%i/%i)" %((float(i+1)/len(userData)*100), i+1, len(userData)))
		sys.stdout.flush()

	print "\r"

main()




