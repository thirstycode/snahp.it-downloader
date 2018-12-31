from bs4 import BeautifulSoup
import requests
import re
import os
from time import time as timer
from multiprocessing.pool import ThreadPool

link = input("Enter link here => ")
directory = input("Enter folder name ==> ")

start = timer()

if not os.path.exists(directory):
    os.makedirs(directory)

homepage = requests.get(link)

all_links = list(set(re.findall(r'http://(.+?)file.html',homepage.text)))

urls = []

def fetch_url(entry):
    path, uri = entry
    r = requests.get(uri, stream=True)
    with open(path, 'wb') as f:
            f.write(r.content)
    return path

for link in all_links:
	res = requests.get("http://" + link + "file.html")
	parts = re.findall(r'.href = (.+?).rar',res.text)
	part1 = re.findall(r'"/d/(.+?)"+',parts[0])
	number = re.findall(part1[0] + '"+' + '(.+[0-9])%1000',parts[0])
	number = int(number[0][2:])
	numberadd = str((number%1000) + 11)
	end = re.findall(r'\+\"/(.*)',parts[0])
	url = part1[0] + numberadd + "/" + end[0] + ".rar"
	urlno = re.findall(r'www(.+?)zippyshare',link)[0]
	url = "http://www" + urlno + "zippyshare.com/d/" + url
	urls.append((directory + "/" + end[0] + ".rar",url))

print("link fetched, starting download...")
results = ThreadPool(8).imap_unordered(fetch_url, urls)
for path in results:
    print(path)

print(f"Elapsed Time: {timer() - start}")