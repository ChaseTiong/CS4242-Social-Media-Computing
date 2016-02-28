import re, csv
from nltk.stem.lancaster import LancasterStemmer

class Helper:
    def __init__(self):
        # Instantiate Stopwords
        self.stopwords = self.getStopwords('data/stopwords.txt')

        # Create featureList, the featurelist are all the unique words appearing in the tweets
        # self.featureList = self.getFeatureList(tweets)
        self.featureList = None

        # Create label dictionary
        self.labelDictionary = None
        # self.labelDictionary = self.createLabelDictionary(tweets)


    def clean(self, tweet):
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',tweet) # Replace links with 'url'
        
        # EMOTICONS
        tweet = re.sub(':\)+','em-smile',tweet) # :) 
        tweet = re.sub(';\)+', 'em-wink', tweet) # ;)
        tweet = re.sub('(:|;)D+', 'em-happy', tweet) # :D ;D
        tweet = re.sub("(:|;)'?\(+",'em-sad', tweet) # :( :'( ;(

        tweet = re.sub("\$\d*", 'price-dollars', tweet)
        # tweet = re.sub("\.{3}", 'trplDot', tweet)  # ...
        tweet = re.sub('\.*', '', tweet) # Remove all dots
        tweet = re.sub('\,*', '', tweet) # Remove all commas
        tweet = re.sub('\!*', '', tweet) # Remove all exclamation marks
        tweet = re.sub('\?*', '', tweet) # Remove all question marks

        tweet = re.sub('[\'\"]', '', tweet) # Remove " and '
        tweet = tweet.lower() # Lowercase tweet
        tweet = re.sub("@(?!google|microsoft|twitter|apple)\S*", '', tweet)
        tweet = tweet.split()
        for i in range(0,len(tweet)):
            tweet[i] = LancasterStemmer().stem(tweet[i])
        tweet = " ".join(tweet)
        return tweet


    def getFeatureList(self, tweets):
        # fl = []
        fl = set()
        for tw in tweets:
            tweet = self.clean(tw[0])
            for word in tweet.split():
                # if word not in self.stopwords and word not in fl:
                    # fl.append(word)
                fl.add(word)
        # print fl
        self.featureList = sorted(fl)
        print "Number of tweets: %i" %(len(tweets))
        print "Feature vector length: %i" %(len(self.featureList))
        return self.featureList

    def getStopwords(self, path_to_stopwords):
        sw = []
        with open(path_to_stopwords) as stopwords:
            for word in stopwords:
                sw.append(word.strip('\r\n'))
        return sw

    def getNBFeatures(self, tweet):
        features = {}
        # tweet = set(self.clean(tweet).split())
        # tweet = set(tweet)
        for word in self.featureList: # Breaking
            features["%s" %word] = (word in tweet)
            # features['contains(%s)' %word] = (word in tweet)
        return features

    def getNBFeatureVector(self, tweet):
        tweet = set(self.clean(tweet).split())
        featureVector = []
        for word in self.featureList:
            if word in tweet:
                featureVector.append(word)
        # print list(featureVector)
        return list(featureVector)

    def getSVMFeatureVector(self, tweet):
        tweet = set(self.clean(tweet).split())
        featureVector = []
        for word in self.featureList:
            if word in tweet:
                featureVector.append(1)
            else:
                featureVector.append(0)
        return featureVector

    def createLabelDictionary(self, tweets):
        labelDict = {}
        labels = set()
        for tweet in tweets:
            labels.add(tweet[1])

        for i in range(0, len(labels)):
            labelDict[list(labels)[i]] = i;
            labelDict[i] = list(labels)[i];

        self.labelDictionary = labelDict
        # return labelDict

    def translateLabel(self, label):
        return self.labelDictionary[label]

    def saveSVMOutput(self, outfile, p_labs, tweets, p_acc, p_vals):
        print "Saving outfile to "+outfile+"..."
        o = open(outfile, 'w')
        headers = ["Tweet", "Correct Sentiment", "Predicted Sentiment"]
        writer = csv.DictWriter(o, fieldnames=headers)
        writer.writeheader()
        for i in range(0, len(p_labs)):
            tweet = list(tweets[i])[0]
            correct_label = list(tweets[i])[1]
            predicted_label = self.translateLabel(int(p_labs[i]))
            writer.writerow({
                headers[0]: self.clean(tweet), 
                headers[1]: correct_label,
                headers[2]: predicted_label})
        o.close()