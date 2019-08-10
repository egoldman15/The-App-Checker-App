from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen
import string
import re
import csv

#====Create Dataset of only US colleges====

# with open('world-universities.csv', 'r', encoding='utf-8') as inp, open('collegeDataset.csv', 'w', encoding='utf-8') as out:
#     writer = csv.writer(out)
#     for row in csv.reader(inp):
#         if row[0] == "US":
#             writer.writerow(row[1:])


##====Getting URLs from Infobox====
def readInfobox(url):
    if "/wiki/" not in url:
        return None
    page2 = urlopen(url)
    soup2 = BeautifulSoup(page2, 'lxml')

    table = soup2.find('table', class_='infobox vcard')
    result = {}
    exceptional_row_count = 0
    if table:
        for tr in table.find_all('tr'):
            if tr.find('th'):
                if tr.find('td'):
                    if tr.find('th').text not in result:
                        result[tr.find('th').text] = tr.find('td').text
            else:
                # the first row Logos fall here
                exceptional_row_count += 1
        return result


# #====Create Dataset of Colloquial Names====
# url = "https://en.wikipedia.org/wiki/List_of_colloquial_names_for_universities_and_colleges_in_the_United_States"
# page = urlopen(url)
# soup = BeautifulSoup(page, 'lxml-xml', from_encoding='utf-8')
# csvData = []
# wikiLinks = []
# collegeDatasetAbbrev = open('collegeDatasetAbbrev.csv', 'w', newline='', encoding='utf-8')
# skipcount = 0
#
# for letter in "ABCDEFGHIJKLMNOPQRSTUVWXY":
#     section = soup.find('span', id=letter).parent
#     liTags = section.find_next('ul').find_all('li')
#
#     for tag in liTags:
#         try:
#             for link in tag.find_all('a'):
#                 row = []
#                 fullName = link.get('title')
#                 abbrev = tag.text.split(' –', 1)[0]
#                 row.append(fullName)
#                 row.extend(abbrev.split(' or '))
#                 url = "https://en.wikipedia.org" + link.get('href')
#                 if readInfobox(url) is not None:
#                     if 'Website' in readInfobox(url):
#                         schoolUrl = readInfobox(url)['Website']
#                         schoolUrl = schoolUrl.replace("https://", "")
#                         schoolUrl = schoolUrl.replace("www.", "")
#                         schoolUrl = schoolUrl.replace("/", "")
#                         row.append(schoolUrl)
#
#                 print(row)
#                 csvData.append(row)
#         except UnicodeEncodeError:
#             skipcount += 1
#             pass
#
# writer = csv.writer(collegeDatasetAbbrev)
# writer.writerows(csvData)
# collegeDatasetAbbrev.close()

# #====Add collegeDatasetAbbrev.csv to collegeDataset.csvData====
# collegeAbbrev = open('collegeDatasetAbbrev.csv', 'r', encoding='utf-8')
# collegeAbbrevReader = csv.reader(collegeAbbrev)
#
# collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
# collegeDatasetReader = csv.reader(collegeDataset)
#
# all = []
# for row in collegeDatasetReader:
#     all.append(row)
#
# for row in all:
#     row[-1] = row[-1].replace("https://", "")
#     row[-1] = row[-1].replace("http://", "")
#     row[-1] = row[-1].replace("www.", "")
#     if row[-1][-1] == '/':
#         row[-1] = row[-1][:-1]
#
# abbrevs = []
# for row in collegeAbbrevReader:
#     abbrevs.append(row)
#
# collegeDataset.close()
# collegeAbbrev.close()
#
# collegeDataset = open('collegeDataset.csv', 'w', encoding='utf-8', newline='\n')
# collegeDatasetWriter = csv.writer(collegeDataset)
#
# count = 0
# check = []
#
# for row in all:
#     for abbrevRow in abbrevs:
#         if abbrevRow[-1] == row[-1] or abbrevRow[0] in row[0]:
#             count+=1
#             # print(row[0], abbrevRow[1:-1])
#             for item in abbrevRow[1:-1]:
#                 row.insert(1, item)
#             check.append(abbrevRow)
#
# # for abbrevRow in abbrevs:
# #     if abbrevRow not in check:
# #         print(abbrevRow)
# #
# # print(count)
#
#
# for row in all:
#     print(row)
#
# collegeDatasetWriter.writerows(all)

# #====Get Team names and Locations====
# #===*Note* Mentions of mascot should be team names===
#
# url = "https://en.wikipedia.org/wiki/List_of_college_team_nicknames_in_the_United_States"
# page = urlopen(url)
# soup = BeautifulSoup(page, 'lxml-xml', from_encoding='utf-8')
# csvData = []
# wikiLinks = []
# collegeDatasetMascots = open('collegeDatasetMascots.csv', 'w', newline='', encoding='utf-8')
# manualLog = open('manualLog.txt', 'w')
# skipcount = 0
# manualCheck = []
# inner_loop_broken = False
#
# liTags = soup.find_all('li')
#
# for tag in liTags:
#     try:
#         if inner_loop_broken == True:
#             break
#         for link in tag.find_all('a'):
#             row = []
#             fullName = link.get('title')
#             if fullName != None:
#                 row.append(fullName)
#             url = "https://en.wikipedia.org" + link.get('href')
#             if readInfobox(url) is not None:
#                 if 'Nickname' in readInfobox(url):
#                     nicknames = re.split(' & | and |, | \(men\) | \(men\)| \\\ | / ',re.sub(r" ?\[[^)]+\]", "", readInfobox(url)['Nickname'].replace(' (women)', '')))
#                     row.extend(nicknames)
#                 if 'Location' in readInfobox(url):
#                     location = readInfobox(url)['Location'].split(',')[0]
#                     row.append(location)
#                     if len(location.split(' ')) > 2:
#                         manualCheck.append(location)
#                 if 'Website' in readInfobox(url):
#                     schoolUrl = readInfobox(url)['Website']
#                     schoolUrl = schoolUrl.replace("https://", "")
#                     schoolUrl = schoolUrl.replace("http:", "")
#                     schoolUrl = schoolUrl.replace("www.", "")
#                     schoolUrl = schoolUrl.replace("/", "")
#                     row.append(schoolUrl)
#
#             if len(row) > 1:
#                 print(row)
#                 csvData.append(row)
#                 if row[0] == "Youngstown State University":
#                     inner_loop_broken = True
#                     break
#
#
#     except UnicodeEncodeError:
#         skipcount += 1
#         pass
#
# writer = csv.writer(collegeDatasetMascots)
# writer.writerows(csvData)
# collegeDatasetMascots.close()
# print(manualCheck)
# for item in manualCheck:
#     manualLog.write(item + '\n')
# manualLog.close()

# #====Add collegeDatasetMascots.csv to collegeDataset.csvData====
# collegeMascot = open('collegeDatasetMascots.csv', 'r', encoding='utf-8')
# collegeMascotReader = csv.reader(collegeMascot)
#
# collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
# collegeDatasetReader = csv.reader(collegeDataset)
#
# notAdded = open('notAdded.txt', 'w')
#
# all = []
# for row in collegeDatasetReader:
#     all.append(row)
#
# mascots = []
# for row in collegeMascotReader:
#     mascots.append(row)
#
# collegeDataset.close()
# collegeMascot.close()
#
# collegeDataset = open('collegeDataset.csv', 'w', encoding='utf-8', newline='\n')
# collegeDatasetWriter = csv.writer(collegeDataset)
#
# count = 0
# check = []
#
# for row in all:
#     for mascotRow in mascots:
#         if mascotRow[-1] == row[-1] or mascotRow[0] == row[0]:
#             count+=1
#             print(row[0], mascotRow[1:-1])
#             for item in mascotRow[1:-1]:
#                 row.insert(1, item)
#             check.append(mascotRow)
#
# for mascotRow in mascots:
#     if mascotRow not in check:
#         print(mascotRow)
#         notAdded.write(",".join(str(x) for x in mascotRow) + '\n')
#
# print(count)
#
# collegeDatasetWriter.writerows(all)

#===Add Clean college names to Dataset===
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
