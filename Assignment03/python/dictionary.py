sentiments = ["positive", "negative", "neutral", "irrelevant"]

sentimentToLabel = {}
labelToSentiment = {}

for i in range(0, len(sentiments)):
	sentimentToLabel[sentiments[i]] = i
	labelToSentiment[i] = sentiments[i]

def translateLabel(label):
	return labelToSentiment[label]

def translateSentiment(sentiment):
	return sentimentToLabel[sentiment]