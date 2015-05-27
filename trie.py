import re, types
from collections import defaultdict

# http://filoxus.blogspot.com/2007/11/trie-in-python.html

def tokenize(s, removePunctuation = True):
    if removePunctuation:
        #p = re.compile('[\.,!?()\[\]{}:;"\'<>/ \n\r\t]')
        p = re.compile('[\.,!?\[\]{}"\'<>/ \n\r\t]')
        return [el for el in p.split(s) if el]
    else:
        t = []
        s = re.split('\s', s)
        p = re.compile('(\W)')
        for phrase in s:
            words = p.split(phrase)
            for word in words:
                t.append(word)
        return [el for el in t if el]

class Node(object):
   
    def __init__(self):
        self.freq = 0
        self.next = defaultdict(int)

class Trie(object):
   
    def __init__(self, inFile):

        self.nodes = []
        self.nodes.append(Node())
        self.n = 1
        self.numberOfWords = 0

        for line in file(inFile):
            words = tokenize(line)
            for w in words:
                currNode = 0
                for char in w:
                    if self.nodes[currNode].next[char] == 0:
                        self.nodes.append(Node())
                        self.nodes[currNode].next[char] = self.n
                        currNode = self.n
                        self.n += 1
                    else:
                        currNode = self.nodes[currNode].next[char]
                self.nodes[currNode].freq += 1
        self.numberOfWords = len([node for node in self.nodes if node.freq != 0])

    def getitem(self, word):
        """Return the frequency of the given word."""

        if isinstance(word, types.StringTypes):
            currNode = 0
            for char in word:
                if self.nodes[currNode].next[char] == 0:
                    #raise AttributeError("No such word: %s" % word)
                    return 0
                else:
                    currNode = self.nodes[currNode].next[char]
            return self.nodes[currNode].freq
        else:
            raise TypeError()

    def len(self):
        """Return the number of nodes in the trie."""

        return self.n