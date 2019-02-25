import requests, numpy
from bs4 import BeautifulSoup
import time

# Defining the user agent
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


# Fetching result from google via the user agent
# returning the html response 
def fetch_results():
    url = 'http://www.oversoeogland.dk/sitemap.asp'
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()

    return response.text

# Method that parse the html results 
# via beatufulSoup and search for the link
# we are look for. 
def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    found_results = []
    result_block = soup.find_all('tr')
    for result in result_block:

        try:
            title = result.find('b')
            link = result.find('a', href=True)['href']

            link = 'http://www.oversoeogland.dk' + link

            if(title == None):
                title = result.find_all('a')[0].text
            else:
                title = title.text


            if title:          #testing for results 
                ##print('## SITE: '+ link)


                found_results.append({'Title':title,'Link':link})
        except:
            print("An exception occurred")

    return found_results


# method that takes a list of keywords, site to seach for, 
# amount of pages to look through.
# returns a list of rank of the page.
def findAllRanks():
    data = parse_results(fetch_results())
    return data


findAllRanks()

import csv
import numpy as np
yourArray = findAllRanks()
yourArray = np.array(yourArray)

'''
with open('outputFile.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in range(0,yourArray.shape[0]):
        myList = []
        myList.append(yourArray[row])
        writer.writerow(myList)


print(findAllRanks())

'''

rows = findAllRanks()

print(rows)

# implement this wrapper on 2.6 or lower if you need to output a header
class DictWriterEx(csv.DictWriter):
    def writeheader(self):
        header = dict(zip(self.fieldnames, self.fieldnames))
        self.writerow(header)

out = open('foo.csv', 'wb')
writer = DictWriterEx(out, fieldnames=['Title','Link'])
# DictWriter.writeheader() was added in 2.7 (use class above for <= 2.6)
writer.writeheader()
for row in rows:
    writer.writerow(dict((k, v.encode('utf-8')) for k, v in row.iteritems()))
out.close()
