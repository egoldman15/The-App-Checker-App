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

#====Get Mascots and Locations====
#===*Note* Mentions of mascot should be team names (Mascots are not checked)===

url = "https://en.wikipedia.org/wiki/List_of_college_team_nicknames_in_the_United_States"
page = urlopen(url)
soup = BeautifulSoup(page, 'lxml-xml', from_encoding='utf-8')
csvData = []
wikiLinks = []
collegeDatasetMascots = open('collegeDatasetMascots.csv', 'w', newline='', encoding='utf-8')
manualLog = open('manualLog.txt', 'w')
skipcount = 0
manualCheck = []
inner_loop_broken = False

liTags = soup.find_all('li')

for tag in liTags:
    try:
        if inner_loop_broken == True:
            break
        for link in tag.find_all('a'):
            row = []
            fullName = link.get('title')
            if fullName != None:
                row.append(fullName)
            url = "https://en.wikipedia.org" + link.get('href')
            if readInfobox(url) is not None:
                if 'Nickname' in readInfobox(url):
                    # Separate all strings where there are two team names and delete Wikipedia citations (i.e. [3])
                    nicknames = re.split(' & | and |, | \(men\) | \(men\)| \\\ | / ',re.sub(r" ?\[[^)]+\]", "", readInfobox(url)['Nickname'].replace(' (women)', '')))
                    row.extend(nicknames)
                if 'Location' in readInfobox(url):
                    location = readInfobox(url)['Location'].split(',')[0]
                    row.append(location)
                    if len(location.split(' ')) > 2:
                        manualCheck.append(location)
                if 'Website' in readInfobox(url):
                    # Make all urls the same format
                    schoolUrl = readInfobox(url)['Website']
                    schoolUrl = schoolUrl.replace("https://", "")
                    schoolUrl = schoolUrl.replace("http:", "")
                    schoolUrl = schoolUrl.replace("www.", "")
                    schoolUrl = schoolUrl.replace("/", "")
                    row.append(schoolUrl)

            if len(row) > 1:
                print(row)
                csvData.append(row)
                # Stop at the last college on the page
                if row[0] == "Youngstown State University":
                    inner_loop_broken = True
                    break


    except UnicodeEncodeError:
        skipcount += 1
        pass

writer = csv.writer(collegeDatasetMascots)
writer.writerows(csvData)
collegeDatasetMascots.close()
print(manualCheck)
for item in manualCheck:
    manualLog.write(item + '\n')
manualLog.close()

#====Add collegeDatasetMascots.csv to collegeDataset.csvData====
collegeMascot = open('collegeDatasetMascots.csv', 'r', encoding='utf-8')
collegeMascotReader = csv.reader(collegeMascot)

collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
collegeDatasetReader = csv.reader(collegeDataset)

notAdded = open('notAdded.txt', 'w')

all = []
for row in collegeDatasetReader:
    all.append(row)

mascots = []
for row in collegeMascotReader:
    mascots.append(row)

collegeDataset.close()
collegeMascot.close()

collegeDataset = open('collegeDataset.csv', 'w', encoding='utf-8', newline='\n')
collegeDatasetWriter = csv.writer(collegeDataset)

count = 0
check = []

for row in all:
    for mascotRow in mascots:
        if mascotRow[-1] == row[-1] or mascotRow[0] == row[0]:
            count+=1
            print(row[0], mascotRow[1:-1])
            for item in mascotRow[1:-1]:
                row.insert(1, item)
            check.append(mascotRow)

for mascotRow in mascots:
    if mascotRow not in check:
        print(mascotRow)
        notAdded.write(",".join(str(x) for x in mascotRow) + '\n')

print(count)

collegeDatasetWriter.writerows(all)
