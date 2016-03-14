import re, csv
from nltk.stem.lancaster import LancasterStemmer

class Helper:
    def __init__(self):
        # Instantiate Stopwords
        self.stopwords = self.getStopwords('data/stopwords.txt')

        # Featurelist = all unique words
        self.featureList = None

        # NB Feature dictionary with words and languages
        self.NBFeatures = {}

        # Dictionaries for information that is not in the featurelist
        self.labelDictionary = None
        self.languageDictionary = None
        self.topicDictionary = None


    def clean(self, tweet):
        # Replace links with 'url'
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',tweet) 
        
        # EMOTICONS
        tweet = re.sub(':\)+','em-smile',tweet) # :) 
        tweet = re.sub(';\)+', 'em-wink', tweet) # ;)
        tweet = re.sub('(:|;)D+', 'em-happy', tweet) # :D ;D
        tweet = re.sub("(:|;)'?\(+",'em-sad', tweet) # :( :'( ;(

        # Summarize all prices ($X) to price-dollars
        tweet = re.sub("\$\d*", 'price-dollars', tweet) 

        tweet = re.sub('\.*', '', tweet) # Remove all dots
        tweet = re.sub('\,*', '', tweet) # Remove all commas
        tweet = re.sub('\!*', '', tweet) # Remove all exclamation marks
        tweet = re.sub('\?*', '', tweet) # Remove all question marks

        tweet = re.sub('[\'\"]', '', tweet) # Remove " and '
        tweet = tweet.lower() # Lowercase tweet
        tweet = re.sub("@(?!google|microsoft|twitter|apple)\S*", '', tweet) # Remove all user mentions that is not related to Google, Microsoft, Apple or Twitter
        tweet = tweet.split()
        # Stem the tweet 
        for i in range(0,len(tweet)):
            tweet[i] = LancasterStemmer().stem(tweet[i])
        tweet = " ".join(tweet)
        return tweet
    
    # def removeStopwords(self, tweet):
    #     tweetWords = tweet.split()
    #     tweet = []
    #     for i in range(0, len(tweetWords)):
    #         if tweetWords[i] not in self.stopwords:
    #             tweet.append(tweetWords[i])
    #     return " ".join(tweet)

    def getFeatureVectorFromTweet(self, tweet):
        features = {}
        tweetText = self.clean(tweet["text"])
        wordFeatures = self.getNBWordFeatures(tweetText)

        tweetLang = tweet["lang"]
        langFeatures = self.getNBLangFeatures(tweetLang)

        # tweetTopic = tweet["topic"]
        # topicFeatures = self.getNBTopicFeatures(tweetTopic)

        features.update(wordFeatures)
        features.update(langFeatures)
        # features.update(topicFeatures)

        return features

    def getNBLangFeatures(self, lang):
        langFeatures = {}
        for l in self.NBFeatures["languages"]:
            langFeatures["language(%s)" %l] = (l == lang)
        return langFeatures

    def getNBTopicFeatures(self, topic):
        topicFeatures = {}
        for t in self.NBFeatures["topics"]:
            topicFeatures["topic(%s)" %t] = (t == topic)
        return topicFeatures

    def getNBWordFeatures(self, tweet):
        features = {}
        for word in self.NBFeatures["words"]:
            features['contains(%s)' %word] = (word in tweet.split())
        return features

    def getNBFeatureList(self, tweets, enableStopwords = False):
        words = set()
        languages = set()
        topics = set()

        for t in tweets:
            text = self.clean(t["text"])
            for word in text.split():
                if enableStopwords:
                    if word not in self.stopwords:
                        words.add(word)
                else:
                    words.add(word)
            languages.add(t["lang"])
            topics.add(t["topic"])

        print "Number of language features: %i" %len(languages)
        print "Number of word features: %i" %len(words)
        print "Number of topic features: %i" %len(topics)

        self.NBFeatures["words"] = words
        self.NBFeatures["topics"] = topics
        self.NBFeatures["languages"] = languages

        return self.NBFeatures

    # Creates a featurelist containing all 
    def getFeatureList(self, tweets, enableStopwords = False):
        fl = set()
        for tw in tweets:
            tweet = self.clean(tw["text"])
            for word in tweet.split():
                if enableStopwords:
                    if word not in self.stopwords:
                        fl.add(word)
                else:
                    fl.add(word)
        self.featureList = sorted(fl)
        print "Number of tweets: %i" %(len(tweets))
        print "Number of word features: %i" %(len(self.featureList))
        return self.featureList

    def getStopwords(self, path_to_stopwords):
        sw = []
        with open(path_to_stopwords) as stopwords:
            for word in stopwords:
                sw.append(LancasterStemmer().stem(word.strip('\r\n')).lower())
        return sw

    def getSVMFeatureVector(self, tweet):
        tweetText = set(self.clean(tweet["text"]).split())
        featureVector = []
        for word in self.featureList:
            if word in tweetText:
                featureVector.append(1)
            else:
                featureVector.append(0)
        featureVector.append(self.languageDictionary[tweet["lang"]])
        featureVector.append(self.topicDictionary[tweet["topic"]])

        return featureVector

    def createDictionaries(self, tweets):
        labelDict = {}
        langDict = {}
        topicDict = {}

        labels = set()
        languages = set()
        topics = set()

        for tweet in tweets:
            labels.add(tweet["sentiment"])
            languages.add(tweet["lang"])
            topics.add(tweet["topic"])

        for i in range(0, len(labels)):
            labelDict[list(labels)[i]] = i
            labelDict[i] = list(labels)[i]

        for i in range(0, len(languages)):
            langDict[list(languages)[i]] = i
            langDict[i] = list(languages)[i]

        for i in range(0, len(topics)):
            topicDict[list(topics)[i]] = i
            topicDict[i] = list(topics)[i]

        self.labelDictionary = labelDict
        self.languageDictionary = langDict
        self.topicDictionary = topicDict

    def translateLabel(self, label):
        return self.labelDictionary[label]

    def saveSVMOutput(self, outfile, p_labs, tweets, p_acc, p_vals):
        print "Saving outfile to "+outfile+"..."
        o = open(outfile, 'w')
        headers = ["Tweet", "Correct Sentiment", "Predicted Sentiment"]
        writer = csv.DictWriter(o, fieldnames=headers)
        writer.writeheader()

        for i in range(0, len(p_labs)):
            correct_label = tweets[i]["sentiment"]
            predicted_label = self.translateLabel(int(p_labs[i]))
            tweetText = self.clean(tweets[i]["text"]).encode('utf-8')
            writer.writerow({
                headers[0]: tweetText, 
                headers[1]: correct_label,
                headers[2]: predicted_label})
        o.close()