from __future__ import division
import numpy as np
import itertools as it
import collections
from sklearn.linear_model import LinearRegression

#Good Turing Implementation
#http://recognize-speech.com/language-model/n-gram-model/good-turing
class CustomLanguageModel:
  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.words ={i:0 for i in set([datum.word for sentence in corpus.corpus for datum in sentence.data])}
    self.pair_words = {i:0 for i in it.product(self.words.keys(), self.words.keys())}
    self.prob_pair_words = self.pair_words
    self.Nc = collections.defaultdict(lambda:0)
    self.train(corpus)
    self.V = len(self.words)
    self.N = reduce(lambda x,y: x+y, self.words.values())
    self.a = 0
    self.b = 0
    self.k = 5
  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    # TODO your code here
    for sentence in corpus.corpus:
        for i in range(0,len(sentence.data)-1):
            wordi = sentence.data[i].word
            wordinext = sentence.data[i+1].word
            pair = (wordi, wordinext)
            self.pair_words[pair]+=1
            if i == len(sentence.data)-2:
                self.words[wordinext]+=1
            self.words[wordi]+=1

    for pair in self.pair_words:
        self.Nc[self.pair_words[pair]]+=1

    model = LinearRegression().fit(np.array(self.Nc.keys()).reshape((len(self.Nc), 1)), np.log(self.Nc.values()))
    self.b, self.a = model.coef_[0], model.intercept_
    zeroNc = [i for i in range(max(self.Nc.keys())) if i not in self.Nc]
    for nc in zeroNc:
        self.Nc[nc] = np.exp(self.a+self.b*np.log(nc))

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in range(1, len(sentence)):
        pair = (sentence[i-1], sentence[i])
        if pair not in self.pair_words:
            score += np.log(self.Nc[1]/self.N)
        else:
            if i <= self.k:
                num = (self.pair_words[pair]+1)*self.Nc[1]*self.Nc[self.pair_words[pair]+1]-self.pair_words[pair]*(self.k+1)*self.Nc[self.k+1]*self.Nc[self.pair_words[pair]]
                denom = self.Nc[self.pair_words[pair]]*(self.Nc[1] - (self.k+1)*self.Nc[self.k+1])
                new_count = num/denom
                #print new_count
                score += np.log(new_count/self.N)
            else:
                score += np.log(self.pair_words[pair]/self.N)

    return score

