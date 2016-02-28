import pickle
import reader
import simpleClassifier
# import nltkClassifier
# import NBClassifier
import sys
from sys import stdin

trainingMode = False

def main():
	if(trainingMode): # Train the Classifiers
		# Training and testing files without corresponding tweets
		original_training_file_name = "data/training.csv"
		original_testing_file_name = "data/testing.csv"

		# Output files with corresponding tweets
		updated_training_file_name = "data/output/training-with-tweets.csv"
		updated_testing_file_name = "data/output/testing-with-tweets.csv"

		# Concatinate the training file with its corresponding tweets
		reader.modifyTrainingFile(original_training_file_name, updated_training_file_name)
		reader.modifyTrainingFile(original_testing_file_name, updated_testing_file_name)

		simple = simpleClassifier.Classifier("data/lexicon/pos.txt", "data/lexicon/neg.txt")
		nb = NBClassifier.Classifier()

		nb.train(updated_testing_file_name)

		classifierPickle = open('SimpleClassifier.pkl', 'wb')
		pickle.dump(simple, classifierPickle, pickle.HIGHEST_PROTOCOL)

		classifierPickle = open('NBClassifier.pkl', 'wb')
		pickle.dump(nb, classifierPickle, pickle.HIGHEST_PROTOCOL)
	else: # Test the classifiers
		simpleClassifierPickle = open('SimpleClassifier.pkl', 'rb')
		simple = pickle.load(simpleClassifierPickle)

		NBClassifierPickle = open('NBClassifier.pkl', 'rb')
		nb = pickle.load(NBClassifierPickle)
		# nb.getClassifier().show_most_informative_features(10)


		# Run NB Classifier with valuation set
		# print("Enter a tweet to be classified, type \"quit\" to exit")
		# while(True):
		# 	user_input = stdin.readline().rstrip()
		# 	if(user_input == "quit"):
		# 		break
		# 	else:
		# 		print(nb.classify_tweet(user_input)) 
		# 		print(simple.classify_tweet(user_input)) 

main()