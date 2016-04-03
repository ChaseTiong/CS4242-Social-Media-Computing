import csv
import sys

numInterest = 20.0
f = open('data/correctLabels.csv', 'rt')
try:
    reader = csv.reader(f)
    labelList = list(reader)
    ##for row in reader:
        ##print row[1]
        
finally:
    f.close()
    
f = open('data/predictedLabels.csv', 'rt')
try:
    reader = csv.reader(f)
    predList = list(reader)
    ##for row in reader:
        ##print row[1]
        
finally:
    f.close()


totalPK = 0.0
totalSK = 0.0

for i in range(len(labelList)):
    matchCountPK =0.0
    matchCountSK =0.0
    for j in range(len(labelList[i])):
        if(labelList[i][j] ==predList[i][j]):
            matchCountSK+=1
        if(labelList[i][j] ==predList[i][j] and labelList[i][j] =='1'):
            matchCountPK+=1        
            
    totalPK+= matchCountPK/numInterest
    totalSK+= matchCountSK/numInterest

PK = totalPK/len(labelList)
SK = totalSK/len(labelList)

print 'S@K(%):' ,SK
print 'P@K(%):' ,PK