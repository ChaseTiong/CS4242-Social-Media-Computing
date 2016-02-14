import sys
import csv
import json

def readTrainingFile(infile, outfile):
	f = open(infile, "r").read().split("\n")
	o = open(outfile, 'w')

	headers = f[0].split(",")
	headers.append("Tweet")
	writer = csv.DictWriter(o, fieldnames=headers)
	writer.writeheader()

	for i in range(1,len(f)-1):
		original_data = f[i].split(",")
		tweet_data_file = open("data/tweets/"+original_data[2].strip('"')+'.json')
		tweet_data = json.load(tweet_data_file)
		tweet_data_file.close()
		tweet_text = json.dumps(tweet_data["text"]).encode("utf-8")
		writer.writerow({headers[0]: original_data[0].strip('"'), headers[1]: original_data[1].strip('"'), headers[2]: original_data[2].strip('"'), headers[3]: tweet_text.strip('"')})
	o.close()

def initiateLexicons():
	positive_lexicon = set()
	with open("data/lexicon/pos.txt") as pos:
		pos_words = pos.read().splitlines()
		for word in pos_words:
			positive_lexicon.add(word)

	negative_lexicon = set()
	with open("data/lexicon/neg.txt") as neg:
		neg_words = neg.read().splitlines()
		for word in neg_words:
			negative_lexicon.add(word)

	return [positive_lexicon, negative_lexicon]