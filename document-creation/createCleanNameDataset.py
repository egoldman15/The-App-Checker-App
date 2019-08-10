#===Add Clean college names (names without "University of", "University", etc) to Dataset===
collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
collegeDatasetReader = csv.reader(collegeDataset)

all = []
for row in collegeDatasetReader:
    all.append(row)

for row in all:
    collegeName = row[0]
    if ' - ' in collegeName:
        print(collegeName.split(' - '))
        for name in collegeName.split(' - '):
            row.insert(1, name.strip())
    elif ' at ' in collegeName:
        print(collegeName.split(' at '))
        for name in collegeName.split(' at '):
            row.insert(1, name.strip())
    elif ', ' in collegeName:
        print(collegeName.split(', '))
        for name in collegeName.split(', '):
            row.insert(1, name.strip())

    if collegeName.split(' ')[-1] == "University":
        print(collegeName.replace('University', ''))
        row.insert(1, collegeName.replace('University', '').strip())
    elif re.split(', | - | at ', collegeName)[0].split(' ')[-1] == "University":
        print(re.split(', | - | at ', collegeName)[0].replace('University', ''))
        row.insert(1, re.split(', | - | at ', collegeName)[0].replace('University', '').strip())
    if collegeName.split(' ')[-1] == "College":
        print(collegeName.replace('College', ''))
        row.insert(1, collegeName.replace('College', '').strip())
    if " ".join(collegeName.split(' ')[0:2]) == "University of":
        print(re.split(', | - | at ',collegeName.replace("University of ", ""))[0])
        row.insert(1, re.split(', | - | at ',collegeName.replace("University of ", ""))[0].strip())
    if " ".join(collegeName.split(' ')[0:2]) == "College of":
        print(re.split(', | - | at ',collegeName.replace("College of ", ""))[0])
        row.insert(1, re.split(', | - | at ',collegeName.replace("College of ", ""))[0].strip())

print('\n\n\n\n')
for row in all:
    print(row)

collegeDataset = open('collegeDataset.csv', 'w', encoding='utf-8', newline='\n')
collegeDatasetWriter = csv.writer(collegeDataset)

collegeDatasetWriter.writerows(all)
