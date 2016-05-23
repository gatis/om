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

num_folds = 10
subset_size = len(all_tweet_array)/num_folds

KF_metrics_accuracy = []
KF_metrics_NEU = []
KF_metrics_POS = []
KF_metrics_NEG = []

for i in range(num_folds):
    testing_this_round = all_tweet_array[i*subset_size:][:subset_size]
    training_this_round = all_tweet_array[:i*subset_size] + all_tweet_array[(i+1)*subset_size:]
    test_tweets = BuildFeatureVector(testing_this_round)
    train_tweets = BuildFeatureVector(training_this_round)
    print len(train_tweets)
    print len(test_tweets)

    training_set = nltk.classify.apply_features(extract_features, train_tweets)
    test_set = nltk.classify.apply_features(extract_features, test_tweets)

    NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

    #NBClassifier.show_most_informative_features(2)

    TestSet(testing_this_round)

    KF_metrics_accuracy.append(nltk.classify.accuracy(NBClassifier, test_set))
    KF_metrics_NEU.append((precision(refSet['NEU'], testSet['NEU']), recall(refSet['NEU'], testSet['NEU']), f_measure(refSet['NEU'], testSet['NEU'])))
    KF_metrics_POS.append((precision(refSet['POZ'], testSet['POZ']), recall(refSet['POZ'], testSet['POZ']), f_measure(refSet['POZ'], testSet['POZ'])))
    KF_metrics_NEG.append((precision(refSet['NEG'], testSet['NEG']), recall(refSet['NEG'], testSet['NEG']), f_measure(refSet['NEG'], testSet['NEG'])))

print 'TEST accuracy:', sum(KF_metrics_accuracy) / float(len(KF_metrics_accuracy))
print ''
print ''
print 'NEU precision:', sum(KF_metrics_NEU[0]) / float(len(KF_metrics_NEU[0]))
print 'NEU recall:', sum(KF_metrics_NEU[1]) / float(len(KF_metrics_NEU[1]))
print 'NEU F-measure:', sum(KF_metrics_NEU[2]) / float(len(KF_metrics_NEU[2]))
print ''
print 'POS precision:', sum(KF_metrics_POS[0]) / float(len(KF_metrics_POS[0]))
print 'POS recall:', sum(KF_metrics_POS[1]) / float(len(KF_metrics_POS[1]))
print 'POS F-measure:', sum(KF_metrics_POS[2]) / float(len(KF_metrics_POS[2]))
print ''
print 'NEG precision:', sum(KF_metrics_NEG[0]) / float(len(KF_metrics_NEG[0]))
print 'NEG recall:', sum(KF_metrics_NEG[1]) / float(len(KF_metrics_NEG[1]))
print 'NEG F-measure:', sum(KF_metrics_NEG[2]) / float(len(KF_metrics_NEG[2]))
print ''

