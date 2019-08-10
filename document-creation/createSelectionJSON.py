import json
import csv

collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
collegeDatasetReader = csv.reader(collegeDataset)

selections = []
for row in collegeDatasetReader:
    selections.append(row[0])

collegeDataset.close()

with open('selections.json', 'w', encoding='utf-8') as f:
    json.dump(selections, f)
