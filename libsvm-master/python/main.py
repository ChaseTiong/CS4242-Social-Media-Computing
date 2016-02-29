import pickle
import helper, reader
import SVMClassifier, simpleClassifier, NBClassifier
import time

def main():
	path_to_training_data = "data/training.csv"
	path_to_testing_data = "data/testing.csv"

	SVM_output_file = "data/output/SVMResult.csv"
	NB_output_file = "data/output/NaiveBayesResult-2.csv"
	Smpl_output_file = "data/output/SimpleResult.csv"

	runSVM = True
	runSimple = True
	runNB = True

	print "Getting data..."
	trainingTweets = reader.getTweets(path_to_training_data)
	testingTweets = reader.getTweets(path_to_testing_data)

	if runSVM:
		print "Instantiating SVM Classifier..."
		svm_c = SVMClassifier.SVMClassifier()
		svm_c.prepareHelper(trainingTweets)

		print "Training SVM Classifier..."
		svm_c.train(trainingTweets)

		print "Classifying testing data using SVM..."
		svm_c.classify(testingTweets, SVM_output_file)

	if runSimple:
		print "Instantiating Simple Classifier..."
		simple_c = simpleClassifier.Classifier("data/lexicon/pos.txt", "data/lexicon/neg.txt")
		
		print "Classifying test data using Simple Classifier..."
		simple_c.classifyDataset(testingTweets, Smpl_output_file)

	if runNB:
		print "Instantiating Naive Bayes Classifier..."
		NaiveBayes_c = NBClassifier.NBClassifier()

		NaiveBayes_c.train(trainingTweets)

		print "Classifying dataset using Naive Bayes Classifier..."
		NaiveBayes_c.classifyDataset(testingTweets, NB_output_file)

	print "Getting stats..."

	print "\n"
	print "------------- Naive Bayes Stats -------------"
	reader.getStats(NB_output_file, "data/output/NBdata.csv", "NB")
	print "\n"

	print "----------------- SVM Stats -----------------"
	reader.getStats(SVM_output_file, "data/output/SVMdata.csv", "SVM")
	print "\n"

	print "---------- Simple Classifier Stats ----------"
	reader.getStats(Smpl_output_file, "data/output/SMPLdata.csv", "Simple")
	print "\n"

	print "------------ Random Forest Stats ------------"
	reader.getStats("data/output/RFResult.csv", "data/output/RFdata.csv", "RF")
	print "\n"

start_time = time.time()
main()
print("Program finished in %-.2f seconds." % (time.time() - start_time))