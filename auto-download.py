from bs4 import BeautifulSoup
import requests, rarfile, io
import re
# from robobrowser import RoboBrowser

link = input("Enter link here => ")

homepage = requests.get(link)
# browser = RoboBrowser(history=True)

# soup = BeautifulSoup(homepage.text, 'lxml')

# all_links = soup.find_all("p")

# print(all_links)

all_links = list(set(re.findall(r'http://(.+?)file.html',homepage.text)))

for link in all_links:
	res = requests.get("http://" + link + "file.html")

	parts = re.findall(r'.href = (.+?).rar',res.text)
	print(parts[0])

	part1 = re.findall(r'"/d/(.+?)"+',parts[0])
	# print(part1)
	number = re.findall(part1[0] + '"+' + '(.+[0-9])%1000',parts[0])
	# print(number)
	number = int(number[0][2:])
	# print(number)
	numberadd = str((number%1000) + 11)
	# print(numberadd)
	end = re.findall(r'\+\"/(.*)',parts[0])
	# print(end)
	url = part1[0] + numberadd + "/" + end[0] + ".rar"
	# print(url)

	urlno = re.findall(r'www(.+?)zippyshare',link)[0]
	# print(urlno)

	url = "http://www" + urlno + "zippyshare.com/d/" + url
	print(url)
	r = requests.get(url)
	with open("new/" + end[0] + ".rar","wb") as file:
		file.write(r.content)
	# z = rarfile.RarFile(io.BytesIO(r.content))
	# z.write("new/" + urlno + ".rar")