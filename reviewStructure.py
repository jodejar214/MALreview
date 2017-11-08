import csv
import matplotlib.pyplot as plt
import numpy as np

num_reviews = 0
paragraphCounts = []
wordsPerParagraph = []
wpp2 = []
totalWords = []
f = open('not10reviews.txt','w')
#parse structure of reviews and get info
with open('animeInfo.csv') as csvfile:
	fieldnames = ['popularity_rank','anime_name', 'average_rating', 'num_members', 'review_1', 'review_2', 'review_3', 'review_4', 'review_5', 'review_6', 'review_7', 'review_8', 'review_9', 'review_10', 'review_score_1', 'review_score_2', 'review_score_3', 'review_score_4', 'review_score_5', 'review_score_6', 'review_score_7', 'review_score_8', 'review_score_9', 'review_score_10', 'review_helpfuls_1', 'review_helpfuls_2', 'review_helpfuls_3', 'review_helpfuls_4', 'review_helpfuls_5', 'review_helpfuls_6', 'review_helpfuls_7', 'review_helpfuls_8', 'review_helpfuls_9', 'review_helpfuls_10']
	reader = csv.DictReader(csvfile, fieldnames=fieldnames)
	for row in reader:
		#check if not upcoming anime
		if row['average_rating'] == 'N/A':
			f.write(str(row['anime_name'])+"\n")
		else:
			#check if 10 reviews
			k = 0
			for i in range(1,11):
				#get review
				field = 'review_'+str(i)
				review = row[field]

				if review != '':
					k+=1

			if k < 10:
				f.write(str(row['anime_name'])+"\n")

				#get only reviews with num helpfuls > avg num helpfuls for anime
				total_helpfuls = 0
				for i in range(1,k+1):
					#get num helpfuls
					field = 'review_helpfuls_'+str(i)
					total_helpfuls += int(row[field])
				avg_helpfuls = total_helpfuls/k

				for i in range(1,k+1):
					#get num helpfuls
					field = 'review_helpfuls_'+str(i)
					num_helpfuls = int(row[field])

					if num_helpfuls >= avg_helpfuls:
						if review != '':
							num_reviews += 1
							#split into paragraphs and remove empty lines
							ps = review.split("<br />")
							paragraphs = []
							for p in ps:
								if p != '':
									paragraphs.append(p)

							#find stats of words per paragraph and total words
							wpp = []
							for p in paragraphs:
								words = p.split(" ")
								wordsPerParagraph.append(len(words))
								wpp.append(len(words))
							wpp2.append(wpp)
							pcount = len(wpp)
							total = sum(wpp)

							paragraphCounts.append(pcount)
							totalWords.append(total)

			else:
				#get stats for each review of anime
				for i in range(1,11):
					#get review
					field = 'review_'+str(i)
					review = row[field]
					
					if review != '':
						num_reviews += 1
						#split into paragraphs and remove empty lines
						ps = review.split("<br />")
						paragraphs = []
						for p in ps:
							if p != '':
								paragraphs.append(p)

						#find stats of words per paragraph and total words
						wpp = []
						for p in paragraphs:
							words = p.split(" ")
							wordsPerParagraph.append(len(words))
							wpp.append(len(words))
						wpp2.append(wpp)
						pcount = len(wpp)
						total = sum(wpp)

						paragraphCounts.append(pcount)
						totalWords.append(total)
f.close()


#get stats and write to file
f = open('stats.txt','w')
f.write("Total Reviews Analyzed: " + str(num_reviews) + "\n\n")
f.write("Stats about Number of Paragraphs:\n")
avgNumParagraphs = sum(paragraphCounts)/len(paragraphCounts)
minNumParagraphs = min(paragraphCounts)
maxNumParagraphs = max(paragraphCounts)
stdNumParagraphs = np.std(paragraphCounts)
f.write(str(avgNumParagraphs) +','+ str(minNumParagraphs) +','+ str(maxNumParagraphs) +','+ str(stdNumParagraphs) + "\n")

f.write("\nStats about Total Words in Review:\n")
avgTotal = sum(totalWords) / len(totalWords)
minTotal = min(totalWords)
maxTotal = max(totalWords)
stdTotal = np.std(totalWords)
f.write(str(avgTotal) +','+ str(minTotal) +','+ str(maxTotal) +','+ str(stdTotal) + "\n")

f.write("\nStats about Number of Words Per Paragraph:\n")
avgPerParagraph = sum(wordsPerParagraph) / len(wordsPerParagraph)
minPerParagraph = min(wordsPerParagraph)
maxPerParagraph = max(wordsPerParagraph)
stdPerParagraph = np.std(wordsPerParagraph)
f.write(str(avgPerParagraph) +','+ str(minPerParagraph) +','+ str(maxPerParagraph) +','+ str(stdPerParagraph) + "\n")

f.write("\nStats About Reviews With Minimum Number of Paragraphs:\n")
minParagraphs = []
for i in range(len(paragraphCounts)):
	if paragraphCounts[i] == minNumParagraphs:
		minParagraphs.append(i)
f.write("Size = " + str(minNumParagraphs) + "\nNumber of reviews = " + str(len(minParagraphs)) + "\n")

minPTotals = []
minWPPs = []
for minParagraph in minParagraphs:
	minPTotal = totalWords[minParagraph]
	minPWPP = sum(wpp2[minParagraph]) / len(wpp2[minParagraph])
	minPTotals.append(minPTotal)
	minWPPs.append(minPWPP)

f.write("\nStats about Total Number of Words for Reviews With Minimum Number of Paragraphs:\n")
avgMinPTotal = sum(minPTotals)/ len(minPTotals)
minMinPTotal = min(minPTotals)
maxMinPTotal = max(minPTotals)
sdMinPTotal = np.std(minPTotals)
f.write(str(avgMinPTotal) +','+ str(minMinPTotal) +','+ str(maxMinPTotal) +','+ str(sdMinPTotal) +  "\n")

f.write("\nStats about Number of Words Per Paragraph for Reviews With Minimum Number of Paragraphs:\n")
avgMinWPP = sum(minWPPs)/ len(minWPPs)
minMinWPP = min(minWPPs)
maxMinWPP = max(minWPPs)
sdMinWPP = np.std(minWPPs)
f.write(str(avgMinWPP) +','+ str(minMinWPP) +','+ str(maxMinWPP) +','+ str(sdMinWPP) +  "\n")

f.write("\nStats With Maximum Number of Paragraphs:\n")
maxParagraphs = []
for i in range(len(paragraphCounts)):
	if paragraphCounts[i] == maxNumParagraphs:
		maxParagraphs.append(i) 
for maxParagraph in maxParagraphs:
	maxPTotal = totalWords[maxParagraph]
	maxPWPP = sum(wpp2[maxParagraph]) / len(wpp2[maxParagraph])
	f.write(str(maxNumParagraphs) +','+ str(maxPTotal) +','+ str(maxPWPP) + "\n")

f.write("\nStats About Reviews With Average Number of Paragraphs:\n")
avgParagraphs = []
for i in range(len(paragraphCounts)):
	if paragraphCounts[i] == avgNumParagraphs:
		avgParagraphs.append(i) 
f.write("Size = " + str(avgNumParagraphs) + "\nNumber of reviews = " + str(len(avgParagraphs)) + "\n")

avgPTotals = []
avgWPPs = []
for avgParagraph in avgParagraphs:
	avgPTotal = totalWords[avgParagraph]
	avgPWPP = sum(wpp2[avgParagraph]) / len(wpp2[avgParagraph])
	avgPTotals.append(avgPTotal)
	avgWPPs.append(avgPWPP)

f.write("\nStats about Total Number of Words for Reviews With Average Number of Paragraphs:\n")
avgAvgPTotal = sum(avgPTotals)/ len(avgPTotals)
minAvgPTotal = min(avgPTotals)
maxAvgPTotal = max(avgPTotals)
sdAvgPTotal = np.std(avgPTotals)
f.write(str(avgAvgPTotal) +','+ str(minAvgPTotal) +','+ str(maxAvgPTotal) +','+ str(sdAvgPTotal) +  "\n")

f.write("\nStats about Number of Words Per Paragraph for Reviews With Average Number of Paragraphs:\n")
avgAvgWPP = sum(avgWPPs)/ len(avgWPPs)
minAvgWPP = min(avgWPPs)
maxAvgWPP = max(avgWPPs)
sdAvgWPP = np.std(minWPPs)
f.write(str(avgAvgWPP) +','+ str(minAvgWPP) +','+ str(maxAvgWPP) +','+ str(sdAvgWPP) +  "\n")


f.write("\nStats About Reviews Within 1sd of Average Number of Paragraphs:\n")
stdParagraphs = []
low = avgNumParagraphs - stdNumParagraphs
high = avgNumParagraphs + stdNumParagraphs
for i in range(len(paragraphCounts)):
	if paragraphCounts[i] >= low and paragraphCounts[i] <= high:
		stdParagraphs.append(i) 
f.write("Size = " + str(low) + " - " + str(high) + "\nNumber of reviews = " + str(len(stdParagraphs)) + "\n")

stdPTotals = []
stdWPPs = []
for stdParagraph in stdParagraphs:
	stdPTotal = totalWords[stdParagraph]
	stdPWPP = sum(wpp2[stdParagraph]) / len(wpp2[stdParagraph])
	stdPTotals.append(stdPTotal)
	stdWPPs.append(stdPWPP)

f.write("\nStats about Total Number of Words for Reviews Within 1sd of Average Number of Paragraphs:\n")
avgStdPTotal = sum(stdPTotals)/ len(stdPTotals)
minStdPTotal = min(stdPTotals)
maxStdPTotal = max(stdPTotals)
sdStdPTotal = np.std(stdPTotals)
f.write(str(avgStdPTotal) +','+ str(minStdPTotal) +','+ str(maxStdPTotal) +','+ str(sdStdPTotal) +  "\n")

f.write("\nStats about Number of Words Per Paragraph for Reviews Within 1sd of Average Number of Paragraphs:\n")
avgStdWPP = sum(stdWPPs)/ len(stdWPPs)
minStdWPP = min(stdWPPs)
maxStdWPP = max(stdWPPs)
sdStdWPP = np.std(stdWPPs)
f.write(str(avgStdWPP) +','+ str(minStdWPP) +','+ str(maxStdWPP) +','+ str(sdStdWPP) +  "\n")



f.write("\nStats about Review With Minimum Total Words:\n")
minTotals = []
for i in range(len(totalWords)):
	if totalWords[i] == minTotal:
		minTotals.append(i)
for minTotal2 in minTotals:
	minTotalP = paragraphCounts[minTotal2]
	minTotalWPP = sum(wpp2[minTotal2]) / len(wpp2[minTotal2])
	f.write(str(minTotal) +','+ str(minTotalP) +','+ str(minTotalWPP) + "\n")

f.write("\nStats about Review With Maximum Total Words:\n")
maxTotals = []
for i in range(len(totalWords)):
	if totalWords[i] == maxTotal:
		maxTotals.append(i)
for maxTotal2 in maxTotals:
	maxTotalP = paragraphCounts[maxTotal2]
	maxTotalWPP = sum(wpp2[maxTotal2]) / len(wpp2[maxTotal2])
	f.write(str(maxTotal) +','+ str(maxTotalP) +','+ str(maxTotalWPP) + "\n")

#draw histograms
plt.hist(paragraphCounts)
plt.title('Number of Paragraphs in Review')
plt.xlabel('Paragraph Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(totalWords)
plt.title('Total Words in a Review')
plt.xlabel('Total Word Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(wordsPerParagraph)
plt.title('Number of Words Per Paragraph')
plt.xlabel('Words Per Paragraph Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(minPTotals)
plt.title('Total Words for Reviews with Minimum Number of Paragraphs')
plt.xlabel('Total Word Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(minWPPs)
plt.title('Average Number of Words Per Paragraph for Reviews with Minimum Number of Paragraphs')
plt.xlabel('Average Words Per Paragraph Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(avgPTotals)
plt.title('Total Words for Reviews with Average Number of Paragraphs')
plt.xlabel('Total Word Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(avgWPPs)
plt.title('Average Number of Words Per Paragraph for Reviews with Average Number of Paragraphs')
plt.xlabel('Average Words Per Paragraph Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(stdPTotals)
plt.title('Total Words for Reviews within 1sd of Average Number of Paragraphs')
plt.xlabel('Total Word Count')
plt.ylabel('Frequency')
plt.show()

plt.hist(stdWPPs)
plt.title('Average Number of Words Per Paragraph for Reviews within 1sd of Average Number of Paragraphs')
plt.xlabel('Average Words Per Paragraph Count')
plt.ylabel('Frequency')
plt.show()

#inconsistent structure as there is high variance in the stats found
#1 word paragraphs can be headers or emphasis on word in review
#short paragraphs 1-20 words exist due to odd structure of reviews = not bound but conventional writing structure
#high variances and standard deviations for data
#no correlation between structures of reviews that make them helpful