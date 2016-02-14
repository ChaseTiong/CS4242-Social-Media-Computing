import reader
import simpleClassifier

def main():
	# Training files without corresponding tweets
	original_training_file_name = "data/training.csv"

	# Output file with corresponding tweets
	updated_training_file_name = "data/output/training-with-tweets.csv"

	# Concatinate the training file with its corresponding tweets
	reader.readTrainingFile(original_training_file_name, updated_training_file_name)

	# Initiate lexicon with positive and negative words
	positive_lexicon, negative_lexicon = reader.initiateLexicons()

	# Output file with classified tweets
	output_file_name = "data/output/simple-classifier-output.csv"

	# Simple classifier using BOW-technique, similar to the one in the Java baseline code providedprint("Correctly classified: "+correctly_classified)
	simpleClassifier.classifyDataset(updated_training_file_name, output_file_name, positive_lexicon, negative_lexicon)

main()