import urllib2
import os
import csv
from HTMLParser import HTMLParser

#gets page of 50 entries from anime chart
def getChart(num,outFile):
	baseurl = "https://myanimelist.net/topanime.php?type=bypopularity&limit="
	aclass = '<a class="hoverinfo_trigger fl-l ml12 mr8" href='
	alen = len(aclass)

	res = urllib2.urlopen(baseurl+str(num))
	html = res.read()
	for i in range(0,50):
		ind = html.index(aclass)
		html = html[ind+alen:]
		space = html.index(" ")
		outFile.write(html[1:space-1]+"\n")

#go to anime's profile and retrieve relevant info
def getAnimeInfo(url):
	ratingTag = '<span itemprop="ratingValue">'
	popTag = '<span class="dark_text">Popularity:</span>'
	membersTag = '<span class="dark_text">Members:</span>'

	#get name from url
	ind = url.rfind("/")
	name = url[ind+1:]
	name = name.replace("_"," ").strip()

	#read html to get other info
	res = urllib2.urlopen(url)
	html = res.read()

	#get rating
	ind = html.find(ratingTag) + len(ratingTag)
	html = html[ind:]
	end = html.find("<")
	rating = float(html[0:end].strip())

	#get popularity rank
	ind = html.find(popTag) + len(popTag)
	html = html[ind:]
	end = html.find("<")
	pop = html[0:end].strip()
	pop = int(pop[1:])

	#get number of people who watched it
	ind = html.find(membersTag) + len(membersTag)
	html = html[ind:]
	end = html.find("<")
	members = int(html[0:end].strip().replace(",",""))
	return [name, pop, rating, members]

#get reviews for anime
def getReviews(url):
	url = url.strip() + "/reviews"
	res = urllib2.urlopen(url)
	html = res.read()

	g = open("ex.txt", "w")
	g.write(html)
	g.close()

	#find permalink for each review
	pind = html.find("permalink")
	ind = html[0:pind].rfind('<a href="') + len('<a href="')
	html = html[ind:]
	end = html.find('"')
	rurl = html[0:end]
	html = html[pind+len("permalink"):]
	
	#get page of review
	res2 = urllib2.urlopen(rurl)
	html2 = res2.read()

#make dict out of info to write into csv
def makeDict(infoList, reviewList):
	csvInfo = {}

	#get anime info
	csv['anime_name'] = infoList[0]
	csv['popularity_rank'] = infoList[1]
	csv['average_rating'] = infoList[2]
	csv['num_members'] = infoList[3]

	#get review info
	for r in reviewList:
		print(r)

#get top 1000 most popular anime profiles
urlFile = "animeUrls.txt"
if os.path.isfile(urlFile):
	print("File of Anime URLs already exists")
else:
	f = open(urlFile, "w")
	for i in range(0,1000,50):
		getChart(i,f)
	f.close()

f = open(urlFile, "r")
urls = f.readlines()
f.close()
getAnimeInfo(urls[0])
getReviews(urls[0])

# with open('animeInfo.csv', 'w') as csvfile:
#     fieldnames = ['popularity_rank','anime_name', 'average_rating', 'num_members', 'review_1', 'review_2', 'review_3', 'review_4', 'review_5', 'review_6', 'review_7', 'review_8', 'review_9', 'review_10', 'review_score_1', 'review_score_2', 'review_score_3', 'review_score_4', 'review_score_5', 'review_score_6', 'review_score_7', 'review_score_8', 'review_score_9', 'review_score_10', 'review_helpfuls_1',, 'review_helpfuls_2', 'review_helpfuls_3', 'review_helpfuls_4', 'review_helpfuls_5', 'review_helpfuls_6', 'review_helpfuls_7', 'review_helpfuls_8', 'review_helpfuls_9', 'review_helpfuls_10']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     for url in urls:
# 		info = getAnimeInfo(url)
#     	writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})