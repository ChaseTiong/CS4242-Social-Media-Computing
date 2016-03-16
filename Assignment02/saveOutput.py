import csv
import pickle

def main():
	predictedLabels = pickle.load(open("outputLabels.pkl", "rb"))
	num_sentiments = len(predictedLabels[0])
	print num_sentiments
	data = []
	for i in range(0, num_sentiments):
		userSentiments = []
		for j in range(0, len(predictedLabels)):
			userSentiments.append(int(predictedLabels[j][i]))
		data.append(userSentiments)

	with open('outputLabels.csv', 'w') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows(data)

	print "Done."


main()