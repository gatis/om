from trie import Trie
import codecs
import unicodedata
import json
import sys
from csv import writer
import re
		
postrie = Trie('poz.final.txt')
negtrie = Trie('neg.final.txt')

def possent(text):
    n = 0
    match = ""
    for i in text.split():
        if postrie.getitem(i)>0:
            n = n+1
            match = match + i + ","
    return (n,match.strip(","))

def negsent(text):
    n = 0
    match = ""
    for i in text.split():
        if negtrie.getitem(i)>0:
            n = n+1
            match = match = match + i + ","
    return (n,match.strip(","))

def cleanup(text):
    text = re.sub(r'[\.,!?\[\]{}"\'<>/\n\r\t]',' ',text)
    text = re.sub('\s{2,}', ' ', text)
    return text.lower()

def evaltweets():
    f = open(sys.argv[1])
    lines_seen = set()
    for line in f:
        try: 
            tweet = line.split("\t")
        except:
            pass
        tw = cleanup(tweet[1])
        print tweet[0],"\t", tweet[1], "\t", possent(tw)[0], "\t", possent(tw)[1], "\t", negsent(tw)[0], "\t", negsent(tw)[1]

evaltweets()