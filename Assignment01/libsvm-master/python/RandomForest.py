# coding: utf-8
import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords

train = pd.read_csv("data/output/training-with-tweets.csv")
test= pd.read_csv('data/output/testing-with-tweets.csv')

def review_to_words( raw_review ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)

    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review).get_text() 

    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)

    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()

    # 4. In Python, searching a set is much faster than searching a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))

    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   

    # 6. Join the words back into one string separated by space, and return the result.
    return( " ".join( meaningful_words )) 

num_reviews = train["Tweet"].size
clean_train_reviews = []

# Loop over each review; create an index i that goes from 0 to the length of the movie review list 
for i in xrange( 0, num_reviews ):
    # Call our function for each one, and add the result to the list of clean reviews
    clean_train_reviews.append( review_to_words( train["Tweet"][i] ) )

num_reviews = test["Tweet"].size
clean_test_reviews=[]
for i in xrange( 0, num_reviews ):
    # Call our function for each one, and add the result to the list of clean reviews
    clean_test_reviews.append( review_to_words( train["Tweet"][i] ) )

print "Creating the bag of words...\n"
from sklearn.feature_extraction.text import CountVectorizer

# Initialize the "CountVectorizer" object, which is scikit-learn's bag of words tool.  
vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 100) 

# fit_transform() does two functions: First, it fits the model and learns the vocabulary; second, it transforms our training data into feature vectors. The input to fit_transform should be a list of strings.
train_data_features = vectorizer.fit_transform(clean_train_reviews)
test_data_features =vectorizer.fit_transform(clean_test_reviews)
# Numpy arrays are easy to work with, so convert the result to an array
train_data_features = train_data_features.toarray()
test_data_features = test_data_features.toarray()

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators = 100)
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import make_scorer,metrics
precision = metrics.precision_score
recall = metrics.recall_score
f1 = metrics.f1_score

rf= rf.fit( train_data_features, train["Sentiment"] )
pred = rf.predict(test_data_features)

rf_precision = precision(test.Sentiment,pred)
rf_recall = recall(test.Sentiment,pred)
rf_f1 = f1(test.Sentiment,pred)

print rf_precision,rf_recall,rf_f1

text = 'I am good today '
clean_test_reviews.append( review_to_words(text) )
print rf.predict(vectorizer.fit_transform(clean_test_reviews).toarray()[len(clean_test_reviews) -1])

print vectorizer.fit_transform(clean_test_reviews).toarray()[clean_test_reviews.count]
print test_data_features[clean_test_reviews.count]

[review_to_words('weclome to our home wefef')]