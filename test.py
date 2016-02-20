import pickle
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re

def processTweet(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end
# stopWords = getStopWordList('C:/Users/kankan/workspace/cs4242/stopwords.txt')




#Read the tweets one by one and process it
import csv
inpTweets = csv.reader(open('data/output/training-with-tweets.csv', 'rb'), delimiter=',', quotechar='"')
featureList = []

tweets = []
for row in inpTweets:
    sentiment = row[1]
    tweet = row[3]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));

# Remove featureList duplicates
featureList = list(set(featureList))    

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

# Extract feature vector for all tweets in one shote

training_set = nltk.classify.util.apply_features(extract_features, tweets)

# Train the classifier
with open('NBClassifier.pkl', 'wb') as output:
    NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
    pickle.dump(NBClassifier, output, pickle.HIGHEST_PROTOCOL)
# NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

# testTweet = 'My Facebook messed up and I had to make a new one so... add me! Haha at least #twitter is reliable'
# processedTestTweet = processTweet(testTweet)
# print NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))

# cross_valid_set = nltk.classify.util.apply_features(extract_features, tweets)

# print NBClassifier.show_most_informative_features(10)

# cross_valid_accuracy = nltk.classify.accuracy(NBClassifier, cross_valid_set)

# refsets = collections.defaultdict(set)
# testsets = collections.defaultdict(set)

# for i, (feats, label) in enumerate(cross_valid_set):
#     refsets[label].add(i)
#     observed = classifier.classify(feats)
#     testsets[observed].add(i)

# print 'Precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
# print 'Recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])