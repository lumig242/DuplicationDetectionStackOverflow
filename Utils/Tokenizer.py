import re
import string
import nltk
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

__stemmer = nltk.stem.porter.PorterStemmer()
_punc_pattern = re.compile('|'.join(map(re.escape, string.punctuation)))


def tokenize_with_preprocess(text):
    """
    Tokenize with preprocessing. Remove all punctuations and apply stemming on the tokens
    :param text: String
    :return: list of tokens
    """
    return map(__stemmer.stem, filter(lambda w: w not in stop,
                                        nltk.word_tokenize(re.sub(_punc_pattern, '', text.lower()))))


def tokenize(text):
    """
    Tokenize without preprocessing
    :param text: String
    :return: list of tokens
    """
    return nltk.word_tokenize(text)
