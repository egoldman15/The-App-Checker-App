from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen
import re
import csv

#====Getting URLs from Infobox====
def readInfobox(url):
    #Makes sure that the url is a wikipedia article
    if "/wiki/" not in url:
        return None
    page2 = urlopen(url)
    soup2 = BeautifulSoup(page2, 'lxml')

    #Locate infobox
    table = soup2.find('table', class_='infobox vcard')
    result = {}
    exceptional_row_count = 0
    if table:
        for tr in table.find_all('tr'):
            if tr.find('th'):
                if tr.find('td'):
                    result[tr.find('th').text] = tr.find('td').text
            else:
                # the first row Logos fall here
                exceptional_row_count += 1
        return result


#====Create Dataset of Colloquial Names====
url = "https://en.wikipedia.org/wiki/List_of_colloquial_names_for_universities_and_colleges_in_the_United_States"
page = urlopen(url)
soup = BeautifulSoup(page, 'lxml-xml', from_encoding='utf-8')
csvData = []
wikiLinks = []
collegeDatasetAbbrev = open('collegeDatasetAbbrev.csv', 'w', newline='', encoding='utf-8')
skipcount = 0

#Iterate through all the headers in the wiki article
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXY":
    section = soup.find('span', id=letter).parent
    liTags = section.find_next('ul').find_all('li')

    for tag in liTags:
        try:
            for link in tag.find_all('a'):
                row = []
                fullName = link.get('title')
                #Separates the text on wikipedia into an array
                abbrev = tag.text.split(' –', 1)[0]
                row.append(fullName)
                #Some articles have more than one abbreviation separated by ' or '
                row.extend(abbrev.split(' or '))
                url = "https://en.wikipedia.org" + link.get('href')
                #Cleans the url
                if readInfobox(url) is not None:
                    if 'Website' in readInfobox(url):
                        schoolUrl = readInfobox(url)['Website']
                        schoolUrl = schoolUrl.replace("https://", "")
                        schoolUrl = schoolUrl.replace("www.", "")
                        schoolUrl = schoolUrl.replace("/", "")
                        row.append(schoolUrl)

                print(row)
                csvData.append(row)
        except UnicodeEncodeError:
            skipcount += 1
            pass

writer = csv.writer(collegeDatasetAbbrev)
writer.writerows(csvData)
collegeDatasetAbbrev.close()

#====Add collegeDatasetAbbrev.csv to collegeDataset.csvData====
collegeAbbrev = open('collegeDatasetAbbrev.csv', 'r', encoding='utf-8')
collegeAbbrevReader = csv.reader(collegeAbbrev)

collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
collegeDatasetReader = csv.reader(collegeDataset)

#Adds rows from collegeDataset.csv to all
all = []
for row in collegeDatasetReader:
    all.append(row)

#Cleans url in collegeDataset
for row in all:
    row[-1] = row[-1].replace("https://", "")
    row[-1] = row[-1].replace("http://", "")
    row[-1] = row[-1].replace("www.", "")
    if row[-1][-1] == '/':
        row[-1] = row[-1][:-1]

#Adds rows from collegeDatasetAbbrev.csv to abbrevs
abbrevs = []
for row in collegeAbbrevReader:
    abbrevs.append(row)

collegeDataset.close()
collegeAbbrev.close()

collegeDataset = open('collegeDataset.csv', 'w', encoding='utf-8', newline='\n')
collegeDatasetWriter = csv.writer(collegeDataset)

count = 0
check = []

#Combines the two csv files matching the items by the college name or by the url
for row in all:
    for abbrevRow in abbrevs:
        if abbrevRow[-1] == row[-1] or abbrevRow[0] in row[0]:
            count+=1
            # print(row[0], abbrevRow[1:-1])
            for item in abbrevRow[1:-1]:
                row.insert(1, item)
            check.append(abbrevRow)

# for abbrevRow in abbrevs:
#     if abbrevRow not in check:
#         print(abbrevRow)
#
# print(count)


for row in all:
    print(row)

collegeDatasetWriter.writerows(all)
