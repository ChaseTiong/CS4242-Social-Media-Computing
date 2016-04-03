# -*- coding: utf-8 -*-
import os, os.path
import sys, json
sys.path.append('/Users/rickardbergeling/GitHub/CS4242-Social-Media-Computing/Assignment03/python/libsvm-master/python')
import svm
import helper as helperClass

helper = helperClass.Helper()

for i in range(1, len(sys.argv)):
	tweet = json.loads(sys.argv[i])
	print tweet["text"]
	print helper.stem(helper.removeStopwords(helper.easyClean(tweet["text"])))