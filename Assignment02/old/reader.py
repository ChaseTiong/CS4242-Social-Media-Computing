# -*- coding: utf-8 -*-
import sys
# import csv
import json
import os, os.path
import re
from pprint import pprint
import helper

def readData(user, helper, path_to_data):
	fbData = open(path_to_data+"/Facebook/U"+str(user)+".txt").read()
	fbData = helper.easyClean(fbData)
	fbData = helper.stem(fbData)
	# print "Facebook data: "+str(len(fbData.split()))+" words"

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
	
	# This one might not be needed
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

	# linkedInExtractions["title"] = title_pattern.findall(linkedInData)[0]
	# linkedInExtractions["industry"] = industry_pattern.findall(linkedInData)[0]
	if(len(linkedInDescription) == 0):
		linkedInExtractions["description"] = ""
	else:
		linkedInExtractions["description"] = linkedInDescription[0]
	# linkedInExtractions["description"] = description_pattern.findall(linkedInData)[0]
	linkedInExtractions["interrests"] = interrests_pattern.findall(linkedInData)
	linkedInExtractions["skills"] = skills_pattern.findall(linkedInData)
	linkedInExtractions["schools"] = schools_pattern.findall(linkedInData)
	linkedInExtractions["majors"] = majors_pattern.findall(linkedInData)
	linkedInExtractions["positions"] = positions_pattern.findall(linkedInData)
	linkedInExtractions["jobDescriptions"] = job_descriptions_pattern.findall(linkedInData)

	# This one might not be needed 
	linkedInExtractions["othersAlsoViewed"] = others_also_viewed_people_in_pattern.findall(linkedInData)

	for i in linkedInExtractions:
		if(type(linkedInExtractions[i])==str):
			linkedInExtractions[i] = helper.removeStopwords(helper.stem(helper.easyClean(linkedInExtractions[i])))
		
		elif(type(linkedInExtractions[i]) == list):
			for j in range(0, len(linkedInExtractions[i])):
				linkedInExtractions[i][j] = helper.removeStopwords(helper.stem(helper.easyClean(linkedInExtractions[i][j])))

	# print "LinkedIn data: "+str(len(linkedInExtractions))+" catergories"
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
						tweetTexts.append(helper.clean(tweet_data[i]["text"]))
			except:
				pass
				# print "No twitter data for user "+str(user)

	twitterExtractions["tweets"] = tweetTexts

	# print "Extracted tweets: "+str(len(twitterExtractions["tweets"]))

	return {"linkedInData": linkedInExtractions, "facebookData":fbData, "twitterData":twitterExtractions}

