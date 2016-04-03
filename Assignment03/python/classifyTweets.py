# -*- coding: utf-8 -*-
import os, os.path
import sys, json
import cStringIO
sys.path.append('/Users/rickardbergeling/GitHub/CS4242-Social-Media-Computing/Assignment03/python/libsvm-master/python')
import svm
import pickle
import dictionary
from svmutil import *
import helper as helperClass

helper = helperClass.Helper("python/data/stopwords.txt")
helper.setFeatureList(pickle.load(open("python/featureList.pkl", "rb")))

featureVectors = []
for i in range(1, len(sys.argv)):
	tweet = json.loads(sys.argv[i])
	featureVectors.append(helper.getFeatureVector(helper.clean(tweet)))

model = svm_load_model('python/tweetClassifier.model')


save_stdout = sys.stdout
sys.stdout = cStringIO.StringIO()
predictedLabels, predictionAccuracy, predictionValues = svm_predict([0]*len(featureVectors), featureVectors, model)
sys.stdout = save_stdout

for label in predictedLabels:
	print dictionary.translateLabel(int(label))