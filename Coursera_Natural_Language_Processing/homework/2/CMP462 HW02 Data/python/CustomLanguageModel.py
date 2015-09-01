from __future__ import division
import numpy as np
import itertools as it

class CustomLanguageModel:
  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.words ={i:0 for i in set([datum.word for sentence in corpus.corpus for datum in sentence.data])}
    self.pair_words = {i:0 for i in it.product(self.words.keys(), self.words.keys())}
    self.prob_pair_words = self.pair_words
    self.Nc = {}
    self.train(corpus)
    self.V = len(self.words)
    self.N = reduce(lambda x,y: x+y, self.words.values())

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
        if self.pair_words[pair] in self.Nc:
            self.Nc[self.pair_words[pair]]+=1
        else:
            self.Nc[self.pair_words[pair]]=1
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
            next_count = self.pair_words[pair]+1
            while next_count not in self.Nc:
                next_count += 1
                if next_count >= max(self.pair_words.values()):
                    next_count = max(self.pair_words.values())
                    break
            new_count = (next_count)*self.Nc[next_count]/self.Nc[self.pair_words[pair]]
            score += np.log(new_count/self.N)
    return score

