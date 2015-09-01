from __future__ import division
import numpy as np

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.words = {}
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    # TODO your code here
    for sentence in corpus.corpus:
        for datum in sentence.data:
            word = datum.word
            if word in self.words:
                self.words[word]+=1
            else:
                self.words[word]=1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    V = len(self.words)#size of vocabulary
    N = reduce(lambda x,y: x+y, self.words.values())#size of corpus
    score = 0.0
    for token in sentence:
        if token in self.words:
            score+= np.log((self.words[token]+1)/(N+V))
        else:
            score+= np.log(1/(N+V))
    return score

