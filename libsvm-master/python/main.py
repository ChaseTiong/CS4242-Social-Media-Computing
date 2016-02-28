import pickle
import helper, reader
import SVMClassifier, simpleClassifier, NBClassifier
import time

def main():
	print "Preparing data..."
	# Append the tweets to the CSV file
	reader.appendTweets('data/training.csv', 'data/output/training-with-tweets.csv')

	# Remove ambiguous information
	trainingTweets = reader.readTweets('data/output/training-with-tweets.csv', 'data/output/training-trimmed.csv')

	print "Instantiating SVM classifier..."
	# Instantiate classifier
	svm_c = SVMClassifier.SVMClassifier()
	svm_c.prepareHelper(trainingTweets)

	print "Training SVM classifier..."
	# Train classifier
	svm_c.train(trainingTweets)

	print "Preparing test data..."
	# Prepare testing data by appending tweets to the CSV file
	reader.appendTweets('data/testing.csv', 'data/output/testing-with-tweets.csv')
	# Get the data from the test file and remove ambiguous information
	testTweets = reader.readTweets('data/output/testing-with-tweets.csv', 'data/output/testing-trimmed.csv')

	print "Classifying test data using SVM..."
	# Run the classifier on the test data
	svm_c.classify(testTweets, 'data/output/SVMResult.csv')

	print "Instantiating simple classifier..."
	simple_c = simpleClassifier.Classifier("data/lexicon/pos.txt", "data/lexicon/neg.txt")
	
	print "Classifying test data using Simple Classifier..."
	simple_c.classifyDataset(testTweets, 'data/output/SimpleResult.csv')
	
	print "Instantiating Naive Bayes classifier..."
	NaiveBayes_c = NBClassifier.NBClassifier()

	print "Training Naive Bayes classifier..."
	NaiveBayes_c.train(trainingTweets)

	print "Classifying test data using Naive Bayes classifier..."
	NaiveBayes_c.classifyDataset(testTweets, 'data/output/NaiveBayesResult.csv')

	print "Getting stats..."

	print "\n"
	print "-------- Naive Bayes Stats --------"
	reader.getStats("data/output/NaiveBayesResult.csv")
	print "\n"

	print "------------ SVM Stats ------------"
	reader.getStats("data/output/SVMResult.csv")
	print "\n"

	print "----- Simple Classifier Stats -----"
	reader.getStats("data/output/SimpleResult.csv")
	print "\n"

start_time = time.time()
main()
print("Program finished in %-.2f seconds." % (time.time() - start_time))