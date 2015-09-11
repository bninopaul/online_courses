from __future__ import division
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import sys
import getopt
import os


class sklearnNaiveBayes(MultinomialNB):
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
    """
    def __init__(self):
      self.train = []
      self.test = []
  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []

  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10

  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here,
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents))
    return result

  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    trainData = []
    testData = []
    splits = []
    trainDir = args[0]
    if len(args) == 1:
      print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fold in range(0, self.numFolds):
        split = self.TrainSplit()
        for fileName in posTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
          example.klass = 'pos'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        for fileName in negTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
          example.klass = 'neg'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        splits.append(split)
    elif len(args) == 2:
      split = self.TrainSplit()
      testDir = args[1]
      print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        split.train.append(example)

      posTestFileNames = os.listdir('%s/pos/' % testDir)
      negTestFileNames = os.listdir('%s/neg/' % testDir)
      for fileName in posTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (testDir, fileName))
        example.klass = 'pos'
        split.test.append(example)
      for fileName in negTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (testDir, fileName))
        example.klass = 'neg'
        split.test.append(example)
      splits.append(split)
    return splits

  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  def filterStopWords(self, words):
    """
    * TODO
    * Filters stop words found in self.stopList.
    """
    stop_words = self.readFile('../data/english.stop')
    return [word for word in words if word not in stop_words]


def main():
  nb = sklearnNaiveBayes()

  # default parameters: no stop word filtering, and
  # training/testing on ../data/imdb1
  if len(sys.argv) < 2:
      options = [('','')]
      args = ['../data/imdb1/']
  else:
      (options, args) = getopt.getopt(sys.argv[1:], 'f')
  if ('-f','') in options:
    nb.FILTER_STOP_WORDS = True

  splits = nb.buildSplits(args)

  avgAccuracy = 0.0
  fold = 0
  list_vocab = [list(set(i.words)) for i in splits[0].train+splits[0].test]
  vocab = list(set(reduce(lambda x,y: x+y, list_vocab)))
  for split in splits:
    classifier = sklearnNaiveBayes()
    features_train = []
    labels_train = []
    for example in split.train:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      features_train.append(str(words)[1:-1])
      labels_train.append(example.klass)
    X_train = CountVectorizer(vocabulary = vocab).fit_transform(features_train).toarray()
    y_train = labels_train
    naivebayes = MultinomialNB()
    naivebayes.fit(X_train, y_train)

    features_test = []
    labels_test = []
    for example in split.test:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      features_test.append(str(words)[1:-1])
      labels_test.append(example.klass)
    X_test = CountVectorizer(vocabulary = vocab).fit_transform(features_test).toarray()
    y_test = labels_test
    accuracy = naivebayes.score(X_test, y_test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy

if __name__ == "__main__":
    main()
