import csv
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SID
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import extract_unigram_feats, mark_negation
from nltk.corpus import movie_reviews

def parse_csv(filename):
	reviews = {}
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			# clean up utf encoding
			title = row[1].decode("utf8").encode("ascii","ignore")
			contents = [body.decode("utf8").encode("ascii","ignore") for body in row[4:14]]
			reviews[title] = contents
	pickle.dump(reviews, open("raw_reviews.p", "w"))
	return reviews

def parse_tokenize_csv(filename):
	reviews = {}
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			# clean up utf encoding
			title = row[1].decode("utf8").encode("ascii","ignore")
			contents = [word_tokenize(body.decode("utf8").encode("ascii","ignore")) for body in row[4:14]]
			reviews[title] = contents
	pickle.dump(reviews, open("reviews.p", "w"))
	return reviews

def ngrams(reviews, n, filename):
	ngram_dict = {}
	for anime in reviews:
		ngrams = []
		for review in reviews[anime]:
			ngram_freq = nltk.FreqDist(nltk.ngrams(review, n))
			ngrams.append(ngram_freq)
		ngram_dict[anime] = ngrams
	pickle.dump(ngram_dict, open(filename, "w"))
	return ngram_dict

def pretrained_sentiment_analysis(raw_reviews):
	'''
	source for vader sentiment analyzer:
	Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
	Sentiment Analysis of Social Media Text. Eighth International Conference on
	Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
	'''
	sid = SID()
	polarity_dict = {}
	for anime in raw_reviews:
		polarity_dict[anime] = [sid.polarity_scores(body) for body in raw_reviews[anime]]
	pickle.dump(polarity_dict, open("pretrained_sentiment.p", "w"))
	return polarity_dict

def trained_sentiment_analysis(reviews):
	'''
	Citation Info 

	This data was first used in Bo Pang and Lillian Lee,
	``A Sentimental Education: Sentiment Analysis Using Subjectivity Summarization 
	Based on Minimum Cuts'',  Proceedings of the ACL, 2004.

	@InProceedings{Pang+Lee:04a,
	  author =       {Bo Pang and Lillian Lee},
	  title =        {A Sentimental Education: Sentiment Analysis Using Subjectivity Summarization Based on Minimum Cuts},
	  booktitle =    "Proceedings of the ACL",
	  year =         2004
	}
	'''
	print "getting training set..."
	analyzer = SentimentAnalyzer()
	pos_sents = [(sent, "pos") for sent in movie_reviews.sents(categories="pos")]
	neg_sents = [(sent, "neg") for sent in movie_reviews.sents(categories="neg")]
	sents = pos_sents + neg_sents
	marked_sents = analyzer.all_words([mark_negation(sent) for sent in sents])
	unigram_features = analyzer.unigram_word_feats(marked_sents)
	analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_features)
	training = analyzer.apply_features(sents)

	print "training..."
	trainer = NaiveBayesClassifier.train
	classifier = analyzer.train(trainer, training)

	print "classifying..."
	sentiment_dict = {}
	for anime in reviews:
		sentiment_dict[anime] = []
		for review in reviews[anime]:
			sentiment_dict[anime].append(analyzer.classify(review))

	print "pickling..."
	pickle.dump(sentiment_dict, open("trained_sentiment.p","w"))
	return sentiment_dict



# raw_reviews = pickle.load(open("raw_reviews.p"))
# print pretrained_sentiment_analysis(raw_reviews)

reviews = pickle.load(open("reviews.p"))
print trained_sentiment_analysis(reviews)


