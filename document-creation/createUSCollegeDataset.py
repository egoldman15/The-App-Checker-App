# ====Create Dataset of only US colleges====
import csv

with open('world-universities.csv', 'r', encoding='utf-8') as inp, open('collegeDataset.csv', 'w', encoding='utf-8') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0] == "US":
            writer.writerow(row[1:])
