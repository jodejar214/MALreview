import urllib2
import os
import csv
import time
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

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
	rating = html[0:end].strip()

	#get popularity rank
	ind = html.find(popTag) + len(popTag)
	html = html[ind:]
	end = html.find("<")
	pop = html[0:end].strip()
	pop = pop[1:]

	#get number of people who watched it
	ind = html.find(membersTag) + len(membersTag)
	html = html[ind:]
	end = html.find("<")
	members = html[0:end].strip().replace(",","")
	return [name, pop, rating, members]

#get reviews for anime
def getReviews(url):
	url = url.strip() + "/reviews"
	print(url)
	res = urllib2.urlopen(url)
	html = res.read()

	review_info = []
	
	#find permalink for top 10 reviews
	rurls = []
	for i in range(10):
		pind = html.find("<small>permalink</small></a>")
		if pind != -1:
			#get tag after link to review
			temp = html[0:pind]
			#get tag with link that is right before pind and truncate to there
			ind = temp.rfind('<a href="') + len('<a href="')
			html = html[ind:]
			#find end of link to get url
			end = html.find('"')
			rurl = html[0:end]
			rurls.append(rurl)
			#get tag after link for next iteration
			pind = html.find("<small>permalink</small></a>")
			html = html[pind+len("<small>permalink</small></a>"):]
		else:
			print("Only found " + str(i) + " reviews for " + str(url))
			break
	
	#go to each review link
	for rurl in rurls:
		print(rurl)
		#get page of review
		try:
			res2 = urllib2.urlopen(rurl)
		except ValueError:
			break
		html2 = res2.read()

		#get number of helpfuls
		help_tag = html2.find('<span id="rhelp')
		html2 = html2[help_tag:]
		end = html2.find('</span>')
		endb = html2.find('>')
		num_help = html2[endb+1:end].strip()

		#get relevant info from review page
		infostart = '<table border="0" width="105" cellpadding="0" cellspacing="0" class="borderClass" style="border-width: 1px;">'
		ind = html2.find(infostart)+len(infostart)
		html2 = html2[ind:]
		ind = html2.find('</div>') + len('</div>')
		scoreText = html2[0:ind].strip()
		end = html2.find('<div id=')
		reviewText = html2[ind:end].strip()

		#get scores
		scoreText = strip_tags(scoreText).strip()
		scoreTitle = ["Overall","Story","Animation","Sound","Character","Enjoyment"]
		scores = []

		for i in range(len(scoreTitle)):
			s = scoreTitle[i]
			if s != "Enjoyment":
				s2 = scoreTitle[i+1]
				ind = scoreText.find(s) + len(s)
				end = scoreText.find(s2)
				txt = scoreText[ind:end].strip()
				scores.append(txt)
			else:
				ind = scoreText.find(s) + len(s)
				txt = scoreText[ind:].strip()
				scores.append(txt)
		try:
			#clean review text but keep line breaks for analysis
			reviewText = HTMLParser().unescape(reviewText).strip()
			reviewText = str(reviewText).replace("\r\n","")
		except UnicodeError:
			g = open("decodingErrors.txt","a+")
			g.write(str(rurl)+"\n")
			g.close()
			reviewText = str(reviewText).replace("\r\n","").strip()

		review_info.append((num_help, scores, reviewText))
	return review_info

#make dict out of info to write into csv
def makeDict(infoList, reviewInfo):
	csvInfo = {}

	#get anime info
	csvInfo['anime_name'] = infoList[0]
	csvInfo['popularity_rank'] = infoList[1]
	csvInfo['average_rating'] = infoList[2]
	csvInfo['num_members'] = infoList[3]

	#get review info
	i = 1
	for r in reviewInfo:
		csvInfo['review_'+str(i)] = r[2]
		csvInfo['review_score_'+str(i)] = '++'.join(r[1]) 
		csvInfo['review_helpfuls_'+str(i)] = str(r[0])
		i+=1
	return csvInfo

#get top 1000 most popular anime profiles
urlFile = "animeUrls.txt"
f = open(urlFile, "w")
for i in range(0,1000,50):
	getChart(i,f)
f.close()
f = open(urlFile, "r")
urls = f.readlines()
f.close()
print("Retrieved URLS of anime")

#write to csv
print("Starting CSV writing")
with open('animeInfo.csv', 'a+') as csvfile:
	fieldnames = ['popularity_rank','anime_name', 'average_rating', 'num_members', 'review_1', 'review_2', 'review_3', 'review_4', 'review_5', 'review_6', 'review_7', 'review_8', 'review_9', 'review_10', 'review_score_1', 'review_score_2', 'review_score_3', 'review_score_4', 'review_score_5', 'review_score_6', 'review_score_7', 'review_score_8', 'review_score_9', 'review_score_10', 'review_helpfuls_1', 'review_helpfuls_2', 'review_helpfuls_3', 'review_helpfuls_4', 'review_helpfuls_5', 'review_helpfuls_6', 'review_helpfuls_7', 'review_helpfuls_8', 'review_helpfuls_9', 'review_helpfuls_10']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	
	for url in urls:
		anime_info = getAnimeInfo(url)
		review_info = getReviews(url)
		info_dict = makeDict(anime_info, review_info)
		writer.writerow(info_dict)
		
print("Finished CSV Writing")