#!/usr/bin/env python
# coding: utf-8

import csv
import lxml
import requests
from datetime import datetime
from bs4 import BeautifulSoup


url = 'http://bbc.com/igbo'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")


# first element on the page has a different class - extract separately
first_elem = soup.find_all('div', class_='TextGridItem-sc-1dvfmi3-6 cLkEbv')

# remaining elements on page
elems = soup.find_all('div', class_='TextGridItem-sc-1dvfmi3-6 fdmIIY')

# add first element to elements list
elems.insert(0, first_elem[0])

# create file with metadata of all elems
items = [["link", "title", "time_downloaded", "time_published"]]

for e in elems:
    try:
        link = str(e).split("href=")[1].split('"')[1]
        title = str(e).split("href=")[1].split('"')[2].split('</')[0].replace(">","")
        time_downloaded = str(datetime.today().strftime('%Y-%m-%d'))
        time_published = str(e).split(" datetime=")[1].split(">")[0].replace('"', "")
    except:
        pass
    item = [link, title, time_downloaded, time_published]
    items.append(item)


# ### NOW TO THE ACTUAL ARTICLES

# gather only article links from today
pagelinks = []
todays_date = str(datetime.today().strftime('%Y-%m-%d'))
# todays_date = '2020-01-28'

for i in items:
    url = i[0]
    if i[3] == todays_date:
        pagelinks.append(['http://bbc.com'+url, i[1], i[2], i[3]])


# get article
items = []

for i, meta in enumerate(pagelinks):
    paragraphtext = []
    page = requests.get(meta[0])
    soup = BeautifulSoup(page.text, 'html.parser')

    # get text
    articlebody = soup.find(class_='story-body__inner')
    articletext = soup.find_all('p')
    for p in articletext[10:]:
        try:
            text = p.get_text()
        except:
            pass
        # combine all paragraphs into article
        paragraphtext.append(text)

    print("[INFO] Article {} of {}".format(i+1, len(pagelinks)))

    # join paragraphs to recreate the article
    article = [' '.join(paragraphtext)]

    # create rows for csv file
    # 'link','title','date_downloaded','date_published','article'
    item = [meta[0], meta[1], meta[2], meta[3], str(article[0])]
    items.append(item)

print("[INFO] Task complete.")

# create csv
output_file = '/Users/apple/igbo_corpus/igbo_bbc_'+todays_date+'.csv'
with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(items)
