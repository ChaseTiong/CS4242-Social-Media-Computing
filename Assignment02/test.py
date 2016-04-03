import os, os.path
import sys
import csv
from pprint import pprint
sys.path.append('/Users/rickardbergeling/GitHub/CS4242-Social-Media-Computing/Assignment02/libsvm-master/python')

linkedInResultFile = "data/outputLabels-linkedInData.csv"
facebookResultFile = "data/outputLabels-linkedInData.csv"
twitterResultFile = "data/outputLabels-linkedInData.csv"

f = open(linkedInResultFile, "r").read().split("\n")
reader = csv.reader( f, delimiter=',', quotechar='"', escapechar='\\')
linkedInPredictions = list(reader)
del linkedInPredictions[len(linkedInPredictions)-1]

for i in range(0, len(linkedInPredictions)):
	for j in range(0, len(linkedInPredictions[i])):
		linkedInPredictions[i][j] = int(linkedInPredictions[i][j])

f = open(facebookResultFile, "r").read().split("\n")
reader = csv.reader( f, delimiter=',', quotechar='"', escapechar='\\')
facebookPredictions = list(reader)
del facebookPredictions[len(facebookPredictions)-1]

for i in range(0, len(facebookPredictions)):
	for j in range(0, len(facebookPredictions[i])):
		facebookPredictions[i][j] = int(facebookPredictions[i][j])

f = open(twitterResultFile, "r").read().split("\n")
reader = csv.reader( f, delimiter=',', quotechar='"', escapechar='\\')
twitterPredictions = list(reader)
del twitterPredictions[len(twitterPredictions)-1]

for i in range(0, len(twitterPredictions)):
	for j in range(0, len(twitterPredictions[i])):
		twitterPredictions[i][j] = int(twitterPredictions[i][j])

print len(linkedInPredictions)
print len(facebookPredictions)
print len(twitterPredictions)
print facebookPredictions[0][0]

categoryVectors = {}
for i in range(0, len(linkedInPredictions[0])):
	categoryVectors[i] = {}

# ska vara en array med arrayer

for i in range(0, len(linkedInPredictions)):
	# Loop through 1-150
	print linkedInPredictions[i][j]

	for j in range(0, len(linkedInPredictions[i])):
		categoryVectors[j].append(linkedInPredictions[i][j])

# pprint(categoryVectors)
