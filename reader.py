import sys
import csv
import json

def modifyTrainingFile(infile, outfile):
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