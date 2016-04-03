# -*- coding: utf-8 -*-
import sys
import csv
import json
import os, os.path
import re
from pprint import pprint
import helper

def readData(user, helper, path_to_data):
	fbData = open(path_to_data+"/Facebook/U"+str(user)+".txt").read()
	fbData = helper.easyClean(fbData)
	fbData = helper.stem(fbData)
	fbData = helper.removeStopwords(fbData)

	linkedInData = open(path_to_data+"/LinkedIn/U"+str(user)+".html").read()
	linkedInExtractions = {}
	title_pattern = re.compile('<p.*class="title"*.>(.*?)<\/p>')
	industry_pattern = re.compile('<a.*?name="industry".*?>(.*?)<\/a>')
	summary_pattern = re.compile('<div class="summary"><p dir="ltr" class="description">([\S\s]*?)<\/div>')
	description_pattern = re.compile('dir="ltr" class="description">([\S\s]*?)<\/p>')
	interrests_pattern = re.compile('<li><a title="Find users with this keyword" href=".*?">([\S\s]*?)<\/a>')
	skills_pattern = re.compile('data-endorsed-item-name="(.*?)">')
	schools_pattern = re.compile('school-name">(.*?)<\/a>')
	majors_pattern = re.compile('<span class="major"><a .*?>(.*?)<\/a>')
	positions_pattern = re.compile('<a title="Learn more about this title" href=.*?>(.*?)<\/a>')
	job_descriptions_pattern = re.compile('<p dir="ltr" class="description summary-field-show-more">(.*?)<\/p>')
	others_also_viewed_people_in_pattern = re.compile('<p class="browse-map-title">(.*?)<\/p>')

	linkedInDescription = description_pattern.findall(linkedInData)
	linkedInTitle = title_pattern.findall(linkedInData)
	linkedInIndustry = industry_pattern.findall(linkedInData)

	if(len(linkedInIndustry) == 0):
		linkedInExtractions["industry"] = ""
	else:
		linkedInExtractions["industry"] = linkedInIndustry[0]

	if(len(linkedInTitle) == 0):
		linkedInExtractions["title"] = ""
	else:
		linkedInExtractions["title"] = linkedInTitle[0]

	if(len(linkedInDescription) == 0):
		linkedInExtractions["description"] = ""
	else:
		linkedInExtractions["description"] = linkedInDescription[0]

	linkedInExtractions["interrests"] = interrests_pattern.findall(linkedInData)
	linkedInExtractions["skills"] = skills_pattern.findall(linkedInData)
	linkedInExtractions["schools"] = schools_pattern.findall(linkedInData)
	linkedInExtractions["majors"] = majors_pattern.findall(linkedInData)
	linkedInExtractions["positions"] = positions_pattern.findall(linkedInData)
	linkedInExtractions["jobDescriptions"] = job_descriptions_pattern.findall(linkedInData)
	linkedInExtractions["othersAlsoViewed"] = others_also_viewed_people_in_pattern.findall(linkedInData)

	for i in linkedInExtractions:
		if(type(linkedInExtractions[i])==str):
			linkedInExtractions[i] = helper.removeStopwords(helper.stem(helper.easyClean(linkedInExtractions[i])))
		
		elif(type(linkedInExtractions[i]) == list):
			for j in range(0, len(linkedInExtractions[i])):
				linkedInExtractions[i][j] = helper.removeStopwords(helper.stem(helper.easyClean(linkedInExtractions[i][j])))

	path_to_tweets = path_to_data+"/Twitter/U"+str(user)

	twitterExtractions = {}
	tweetTexts = []

	# Read tweets
	for twitterJsonFile in os.listdir(path_to_tweets):
		if(twitterJsonFile != ".DS_Store"):
			try:
				tweet_data = json.load(open(path_to_tweets+"/"+twitterJsonFile))
				for i in range(0, len(tweet_data)-1):
					if(tweet_data[i]["in_reply_to_status_id"]!=None):
						if(tweet_data[i]["lang"]=="en"):
							tweetTexts.append(helper.removeStopwords(helper.stem(helper.easyClean(tweet_data[i]["text"]))))
			except:
				pass
	
	twitterExtractions["tweets"] = tweetTexts
	
	try:
		twitter_data = json.load(open(path_to_tweets+"/"+"1.json"))
		twitterExtractions["userDescription"] = helper.removeStopwords(helper.stem(helper.easyClean(twitter_data[0]["user"]["description"])))
	except:
		twitterExtractions["userDescription"] = ""

	return {"linkedInData": linkedInExtractions, "facebookData":fbData, "twitterData":twitterExtractions}

def saveOutput(predictedLabels, destination):
	num_sentiments = len(predictedLabels[0])
	print num_sentiments
	data = []
	for i in range(0, num_sentiments):
		userSentiments = []
		for j in range(0, len(predictedLabels)):
			userSentiments.append(int(predictedLabels[j][i]))
		data.append(userSentiments)

	with open(destination, 'w') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows(data)

def getSaK():
	numInterest = 20.0
	f = open('correctLabels.csv', 'rt')
	try:
	    reader = csv.reader(f)
	    labelList = list(reader)
	        
	finally:
	    f.close()
	    
	f = open('outputLabels.csv', 'rt')
	try:
	    reader = csv.reader(f)
	    predList = list(reader)
	    ##for row in reader:
	        ##print row[1]
	        
	finally:
	    f.close()


	totalPK = 0.0
	totalSK = 0.0

	for i in range(len(labelList)):
	    matchCountPK =0.0
	    matchCountSK =0.0
	    for j in range(len(labelList[i])):
	        if(labelList[i][j] ==predList[i][j]):
	            matchCountSK+=1
	        if(labelList[i][j] ==predList[i][j] and labelList[i][j] =='1'):
	            matchCountPK+=1        
	            
	    totalPK+= matchCountPK/numInterest
	    totalSK+= matchCountSK/numInterest

	PK = totalPK/len(labelList)
	SK = totalSK/len(labelList)

	print 'S@K(%):' ,SK
	print 'P@K(%):' ,PK
