# -*- coding: utf-8 -*-
import re
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
from pprint import pprint

class Helper:
	def __init__(self, path_to_stopwords="data/stopwords.txt"):
		self.stopwords = self.getStopwords(path_to_stopwords) 
		self.featureList = set()
		print "Helper initialized!"

	def getStopwords(self, path_to_stopwords):
		sw = []
		with open(path_to_stopwords) as stopwords:
			for word in stopwords:
				sw.append(LancasterStemmer().stem(word.strip('\r\n')).lower())
		return sw

	def removeStopwords(self, text):
		text = text.split()
		updatedText = [x for x in text if not x in self.stopwords]
		return " ".join(updatedText)

	# Cleaner copied from previous assignment, well suited for tweets but not as good for formal text
	def clean(self, text):
		# Remove URLS
		text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text)

		# EMOTICONS
		text = re.sub(':-?\)+','em-smile',text) # :) 
		text = re.sub(';-?\)+', 'em-wink', text) # ;)
		text = re.sub('(:|;)-?D+', 'em-happy', text) # :D ;D
		text = re.sub("(:|;)'?-?\(+",'em-sad', text) # :( :'( ;(

		# Summarize all prices ($X) to price-dollars
		text = re.sub("\$\d*", 'price-dollars', text) 

		text = re.sub('\.*', '', text) # Remove all dots
		text = re.sub('\,*', '', text) # Remove all commas
		text = re.sub('\!*', '', text) # Remove all exclamation marks
		text = re.sub('\?*', '', text) # Remove all question marks

		text = re.sub('[\'\"]', '', text) # Remove " and '
		text = text.lower() # Lowercase text
		text = re.sub("@\S*", '', text) # Remove user mentions

		text = self.stem(text)
		return text

	def removeTags(self, text):
		text = re.sub('<.*?>','',text)
		return text

	def easyClean(self, text):
		text = text.lower()
		text = re.sub("(\W)", ' ', text) # Remove any non-word character and replace with a space
		text = re.sub('(\s\d{1,}\s)', ' ',text) # Remove digits surrounded by spaces
		text = re.sub('\d{0,3}?\.?\:?\d{0,2}[ap]m', '',text) # Remove times
		text = re.sub('\s\S\s', ' ', text) # Remove single character "words"
		text = re.sub('(?<=\s)\w*?\d\w*?(?=\s)', '', text)
		# text = re.sub('(?<=\s)\d*?(?=\s)', ' ',text) # Remove digits without context
		text = re.sub('\s{2,}', ' ', text) # Remove extraneous spaces
		return text

	def stem(self, text):
		text = text.split()
		for i in range(0, len(text)):
			# text[i] = LancasterStemmer().stem(text[i])
			text[i] = PorterStemmer().stem(text[i])
		stemmedText = " ".join(text)
		return stemmedText
		return text

	def getUserWords(self, userData):
		return self.recursiveGathering(userData, set())

	def extractWords(self, text):
		words = set()
		for word in text.split():
			words.add(word)
		return words

	def recursiveGathering(self, data, toBeReturned):
		if(type(data)==str):
			data = unicode(data, 'utf-8')

		if(type(data)==str or type(data)==unicode):
			toBeReturned = toBeReturned.union(set(data.split()))

		elif(type(data)==list):
			for i in range(0, len(data)):
				toBeReturned = toBeReturned.union(self.recursiveGathering(data[i], toBeReturned))

		elif(type(data)==dict):
			for key in data:
				toBeReturned = toBeReturned.union(self.recursiveGathering(data[key], toBeReturned))
		else:
			raise ValueError("Unknown data type"+str(type(data)))

		return toBeReturned

	def setFeatureList(self, featureList):
		self.featureList = featureList

	def getFeatureVector(self, text):
		featureVector = []
		for word in self.featureList:
			if word in text:
				featureVector.append(1)
			else:
				featureVector.append(0)
		return featureVector

	def getLabelVectors(self, labelData):
		f = open(labelData, "r").read().split()
		labelVectors = {}

		for i in range(0, len(f[0].split(","))):
			labelVectors[i] = []

		for i in range(0, len(f)):
			for j in range(0, len(f[i].split(","))):
				labelVectors[j].append(int(f[i].split(",")[j]))

		return labelVectors