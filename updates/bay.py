from trie import Trie
import codecs
import unicodedata, collections
import json
import sys
from csv import writer
import re
import nltk
from nltk import precision, recall, f_measure, accuracy, ConfusionMatrix

stopWords = Trie('stopwords.txt')
featureList = []
all_tweet_array = []
train_tweets = []
test_tweets = []
#sets for precision calculation
refSet = collections.defaultdict(set)
testSet = collections.defaultdict(set)	
refSetF = []
testSetF = []

def cleanup(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text)
    #text = re.sub(r'[\.,!?\[\]{}"\'<>/\n\r\t]',' ',text)
    #remove ():; from noisy-labeled set to exclude emoticons
    text = re.sub(r'[\.,!?\[\]{}"\'<>/\n\r\t():;0123456789]',' ',text)
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
        if ((stopWords.getitem(w.lower().encode("utf8"))==0) and val is None):
            featureVector.append(w)
    return featureVector

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['has(%s)' % word] = (word in tweet_words)
    return features

def ReadTweetFileInArr():
    f = open(sys.argv[1]) # pass training and test set
    for line in f:
        try: 
            tweet = line.split("\t")
        except:
            pass
        sentiment = tweet[2][0:3]
        all_tweet_array.append((tweet[0], cleanup(tweet[1]), sentiment))

def BuildFeatureVector(content):
    fw_tweets = []
    for line in content:
        tw = line[1]
        sentiment = line[2]
        featureVector = getFeatureVector(tw)
        featureList.extend(featureVector)
        fw_tweets.append((featureVector, sentiment))
    return fw_tweets

def TestSet(content):
    for line in content:
        tw = line[1]
        correct_sentiment = line[2]
        predicted_sentiment = NBClassifier.classify(extract_features(getFeatureVector(tw)))
        refSet[correct_sentiment].add(line[0])
        testSet[predicted_sentiment].add(line[0])
        refSetF.append(correct_sentiment)
        testSetF.append(predicted_sentiment)
        #print line[0], "\t", predicted_sentiment, correct_sentiment, correct_sentiment == predicted_sentiment


#read file
ReadTweetFileInArr()

training_size = int(round(len(all_tweet_array)*0.8, 0))
test_size = int(round(len(all_tweet_array)*0.2, 0))

print 'Tweets total: %s, train set 80proc: %s, test set 20proc: %s' %(len(all_tweet_array),training_size, test_size)

train_tweets = BuildFeatureVector(all_tweet_array[:training_size])

print len(train_tweets)

test_tweets = BuildFeatureVector(all_tweet_array[training_size:])

print len(test_tweets)

training_set = nltk.classify.apply_features(extract_features, train_tweets)
test_set = nltk.classify.apply_features(extract_features, test_tweets)

NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

NBClassifier.show_most_informative_features(20)

TestSet(all_tweet_array[training_size:])

print ''
print 'TRAINING accuracy:', nltk.classify.accuracy(NBClassifier, training_set)
print 'TEST accuracy:', nltk.classify.accuracy(NBClassifier, test_set)
print ''
print 'NEU precision:', precision(refSet['NEU'], testSet['NEU'])
print 'NEU recall:', recall(refSet['NEU'], testSet['NEU'])
print 'NEU F-measure:', f_measure(refSet['NEU'], testSet['NEU'])
print ''
print 'POS precision:', precision(refSet['POZ'], testSet['POZ'])
print 'POS recall:', recall(refSet['POZ'], testSet['POZ'])
print 'POS F-measure:', f_measure(refSet['POZ'], testSet['POZ'])
print ''
print 'NEG precision:', precision(refSet['NEG'], testSet['NEG'])
print 'NEG recall:', recall(refSet['NEG'], testSet['NEG'])
print 'NEG F-measure:', f_measure(refSet['NEG'], testSet['NEG'])
print ''
print ConfusionMatrix(refSetF, testSetF)

