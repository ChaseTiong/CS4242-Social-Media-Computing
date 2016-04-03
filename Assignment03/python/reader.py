# -*- coding: utf-8 -*-
import csv

def CSVtoArrays(path_to_csv, containsHeaders=False):
	toBeReturned = {}

	f = open(path_to_csv, 'rb')
	reader = csv.reader(f, delimiter=";")

	if(containsHeaders):
		headers = reader.next()
	else:
		headers = []
		for i in range(0, len(reader.next())):
			headers.append(i)
		f.seek(0)
		reader = csv.reader(f, delimiter=";")

	for h in headers:
		toBeReturned[h] = []

	for row in reader:
		for h, v in zip(headers, row):
			toBeReturned[h].append(v)

	return toBeReturned