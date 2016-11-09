import os
import itertools
from collections import Counter

try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
import lda

DUMP_MODEL_PATH = 'lda_model.pkl'


class LDA(object):
    def __init__(self, corpus, load=False, n_topic=3):
        self.words = np.array(list(set(itertools.chain(*corpus))))
        X = np.array(map(self._transform, corpus))

        if not load or not os.path.isfile(DUMP_MODEL_PATH):
            self._model = lda.LDA(n_topics=n_topic, random_state=0, n_iter=100)
            self._model.fit(X)
            with open(DUMP_MODEL_PATH, 'wb') as f:
                pickle.dump(self._model, f)
        else:
            with open(DUMP_MODEL_PATH, 'rb') as f:
                self._model = pickle.load(f)

    def get_lda_model(self):
        """
        :param corpus: list of sets(tokens)
        """
        return self._model

    def _transform(self, tokens):
        counter = Counter(tokens)
        return np.array([counter[w] for w in self.words])

    def get_topic(self, tokens):
        return self._model.transform(self._transform(tokens))

    def get_topic_distribution(self):
        return self._model.topic_word_

    def print_topic_top_words(self, n_top_words=8):
        for i, topic_dist in enumerate(self.get_topic_distribution()):
            topic_words = self.words[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
            print 'Topic {}: {}'.format(i, ' '.join(topic_words))


if __name__ == '__main__':
    from Tokenizer import tokenize_with_preprocess
    corpus = ['Where can I found Stasckoverflow open source dataset?',
              'how to extract tar.7z files from command line?',
              'Obama reminded people of his statement from yesterday that the sun will come up again in the morning:',
              'Davis puts up massive numbers - 31 points per game on 50 percent shooting']
    l = LDA(map(tokenize_with_preprocess, corpus))
    model = l.get_lda_model()
    l.print_topic_top_words()
    print l.get_topic_distribution()
    print l.get_topic(tokenize_with_preprocess('The following demonstrates how to inspect\
        a model of a subset of the Reuters news dataset'))
