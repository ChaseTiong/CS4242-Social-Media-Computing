import helper as h
import reader
from pprint import pprint

def main():
	helper = h.Helper()
	user1Data = reader.readData(5, helper, "data/Train")
	pprint(user1Data)


main()