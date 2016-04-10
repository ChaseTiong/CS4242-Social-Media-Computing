# -*- coding: utf-8 -*-
import re
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
from pprint import pprint

class Helper:
	def __init__(self, path_to_stopwords="data/stopwords.txt"):
		self.stopwords = self.getStopwords(path_to_stopwords) 
		self.featureList = set()

		try:
		    # Wide UCS-4 build
		    self.myre = re.compile(u'['u'\U0001f60D-\U0001f60D]+', re.UNICODE)
		except re.error:
		    # Narrow UCS-2 build
		    self.myre = re.compile(u'('
		        u'\ud83c[\udf00-\udfff]|'
		        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
		        u'[\u2600-\u26FF\u2700-\u27BF])+', 
		        re.UNICODE)

	def getStopwords(self, path_to_stopwords):
		sw = set()
		with open(path_to_stopwords) as stopwords:
			for word in stopwords:
				sw.add(LancasterStemmer().stem(word.strip('\r\n')).lower())
		return sw

	def removeStopwords(self, text):
		updatedText = [x for x in text.split() if not x in self.stopwords]
		return " ".join(updatedText)


	def translateEmojis(self, text):
		# text = self.myre.sub('EMOJIII!', text)
		re.sub(u'\U0001f60D',"positiveSmiley",text)
		re.sub(u'\U0001f601',"positiveSmiley",text)
		re.sub(u'\U0001f602',"positiveSmiley",text)
		re.sub(u'\U0001f603',"positiveSmiley",text)
		re.sub(u'\U0001f604',"positiveSmiley",text)
		re.sub(u'\U0001f605',"positiveSmiley",text)
		re.sub(u'\U0001f606',"positiveSmiley",text)
		re.sub(u'\U0001f607',"positiveSmiley",text)
		re.sub(u'\U0001f609',"positiveSmiley",text)
		re.sub(u'\U0001f618',"positiveSmiley",text)
		re.sub(u'\U0001f62C',"positiveSmiley",text)
		re.sub(u'\U0001f617',"positiveSmiley",text)
		re.sub(u'\U0001f619',"positiveSmiley",text)
		re.sub(u'\U0001f61A',"positiveSmiley",text)
		re.sub(u'\U0001f61B',"positiveSmiley",text)
		re.sub(u'\U0001f61C',"positiveSmiley",text)
		re.sub(u'\U0001f61D',"positiveSmiley",text)
		re.sub(u'\U0001f638',"positiveSmiley",text)
		re.sub(u'\U0001f639',"positiveSmiley",text)
		re.sub(u'\U0001f63A',"positiveSmiley",text)
		re.sub(u'\U0001f63B',"positiveSmiley",text)
		re.sub(u'\U0001f63D',"positiveSmiley",text)
		re.sub(u'\U0001f642',"positiveSmiley",text)
		re.sub(u'\U0001f643',"positiveSmiley",text)
		re.sub(u'\U0001f648',"positiveSmiley",text)
		re.sub(u'\U0001f649',"positiveSmiley",text)
		re.sub(u'\U0001f64A',"positiveSmiley",text)
		re.sub(u'\U0001f646',"positiveSmiley",text)
		re.sub(u'\U0001f64B',"positiveSmiley",text)

		re.sub(u'\U0001f616', "negativeSmiley", text)
		re.sub(u'\U0001f610', "negativeSmiley", text)
		re.sub(u'\U0001f611', "negativeSmiley", text)
		re.sub(u'\U0001f612', "negativeSmiley", text)
		re.sub(u'\U0001f613', "negativeSmiley", text)
		re.sub(u'\U0001f614', "negativeSmiley", text)
		re.sub(u'\U0001f615', "negativeSmiley", text)
		re.sub(u'\U0001f61E', "negativeSmiley", text)
		re.sub(u'\U0001f61F', "negativeSmiley", text)
		re.sub(u'\U0001f622', "negativeSmiley", text)
		re.sub(u'\U0001f623', "negativeSmiley", text)
		re.sub(u'\U0001f624', "negativeSmiley", text)
		re.sub(u'\U0001f625', "negativeSmiley", text)
		re.sub(u'\U0001f626', "negativeSmiley", text)
		re.sub(u'\U0001f627', "negativeSmiley", text)
		re.sub(u'\U0001f628', "negativeSmiley", text)
		re.sub(u'\U0001f629', "negativeSmiley", text)
		re.sub(u'\U0001f62A', "negativeSmiley", text)
		re.sub(u'\U0001f62B', "negativeSmiley", text)
		re.sub(u'\U0001f62D', "negativeSmiley", text)
		re.sub(u'\U0001f620', "negativeSmiley", text)
		re.sub(u'\U0001f621', "negativeSmiley", text)

		re.sub(u'\U0001f62E', "surprisedSmiley", text)
		re.sub(u'\U0001f62F', "surprisedSmiley", text)
		re.sub(u'\U0001f630', "surprisedSmiley", text)
		re.sub(u'\U0001f631', "surprisedSmiley", text)
		re.sub(u'\U0001f632', "surprisedSmiley", text)
		re.sub(u'\U0001f633', "surprisedSmiley", text)
		re.sub(u'\U0001f634', "surprisedSmiley", text)
		re.sub(u'\U0001f635', "surprisedSmiley", text)
		re.sub(u'\U0001f637', "surprisedSmiley", text)
		re.sub(u'\U0001f63E', "surprisedSmiley", text)
		re.sub(u'\U0001f63F', "surprisedSmiley", text)
		re.sub(u'\U0001f641', "surprisedSmiley", text)
		re.sub(u'\U0001f640', "surprisedSmiley", text)
		return text


	def easyClean(self, text):
		text = text.lower()
		text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text)
		text = re.sub("@\S*", '', text) # Remove user mentions
		text = re.sub(':-?\)+','em-smile',text) # :) 
		text = re.sub(';-?\)+', 'em-wink', text) # ;)
		text = re.sub('(:|;)-?D+', 'em-happy', text) # :D ;D
		text = re.sub("(:|;)'?-?\(+",'em-sad', text) # :( :'( ;(
		text = re.sub("(\W)", ' ', text) # Remove any non-word character and replace with a space
		text = re.sub('(\s\d{1,}\s)', ' ',text) # Remove digits surrounded by spaces
		text = re.sub('\d{0,3}?\.?\:?\d{0,2}[ap]m', '',text) # Remove times
		text = re.sub('\s\S\s', ' ', text) # Remove single character "words"
		text = re.sub('(?<=\s)\w*?\d\w*?(?=\s)', '', text)
		text = re.sub('(?<=\s)\d*?(?=\s)', ' ',text) # Remove digits without context
		text = re.sub('\s{2,}', ' ', text) # Remove extraneous spaces
		return text

	def stem(self, text):
		text = text.split()
		for i in range(0, len(text)):
			# text[i] = PorterStemmer().stem(text[i])
			text[i] = LancasterStemmer().stem(text[i])
		stemmedText = " ".join(text)
		return stemmedText
		return text

	def clean(self, text):
		return self.removeStopwords(self.stem(self.easyClean(text)))

	def extractWords(self, text):
		words = set()
		for word in text.split():
			words.add(word)
		return words

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