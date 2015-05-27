from trie import Trie
import codecs
import unicodedata
import json
import sys
from csv import writer
import re
import nltk

stopWords = Trie('stopwords.txt')
featureList = []
tweets = []

def cleanup(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',text)
    text = re.sub(r'[\.,!?\[\]{}"\'<>/\n\r\t]',' ',text)
    text = re.sub('\s{2,}', ' ', text)
    return text.lower().decode("utf8")

def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #check if the word stats with an alphabet
        val = re.search(r"[@#]", w)
        #ignore if it is a stop word or hashtag
        if ((stopWords.getitem(w)==0) and val is None):
            featureVector.append(w)
    return featureVector

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def ReadTrainingSet():
    f = open(sys.argv[1]) # pass training set as first parameter
    for line in f:
        try: 
            tweet = line.split("\t")
        except:
            pass
        tw = cleanup(tweet[1])
        sentiment = tweet[2]
        featureVector = getFeatureVector(tw)
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment));

def TestSet():
    f = open(sys.argv[2]) # pass test set as second parameter
    for line in f:
        try: 
            tweet = line.split("\t")
        except:
            pass
        tw = cleanup(tweet[1])
        print tweet[0], "\t", NBClassifier.classify(extract_features(getFeatureVector(tw)))

ReadTrainingSet()

featureList = list(set(featureList))
training_set = nltk.classify.apply_features(extract_features, tweets)
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

TestSet()
