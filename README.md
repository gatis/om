# om
Resources for opinion mining for written content classification in Latvian text

This is set of work-products to use for opinion mining for written content classification in Latvian text

analyze-lexicon.py - take positive and negative words from lexicon and look for them in tweets

analyze-nb.py - use NB implementation of python-nltk, train NB classifier using data in file in first parameter and then use to detect sentiment in file in second parameter

data/psgs_norm.arff - set of labeled tweets in weka arff format (1-1777 from https://github.com/FnTm/latvian-tweet-sentiment-corpus, rest noisy-labeled by me)

data/TweetSetLV.xlsx - 90171 tweets in LV and result when applied lexicon as in in data/ using analyze-lexicon.py

lexicon/neg.final - negative polarity words in LV

lexicon/neg.final - positive polarity words in LV

stopwords.txt - common LV words with no sentiment

trie.py - Trie implenentation in Py - used in analyze-lexicon.py (from http://filoxus.blogspot.com/2007/11/trie-in-python.html)