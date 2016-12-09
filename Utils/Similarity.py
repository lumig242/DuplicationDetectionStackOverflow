import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine


class _SimilarityUtil(object):
    _vectorizer = TfidfVectorizer(tokenizer=lambda x: x, stop_words='english')

    @staticmethod
    def jaccard_similarity(text1, text2):
        """
        :param text1, text2: list of tokens
        :return: float
        """
        _s1, _s2 = set(text1), set(text2)
        return 1.0 - float(len(_s1 & _s2)) / len(_s1 | _s2)

    @staticmethod
    def _inverse(tokens):
        return ' '.join(tokens)

    @staticmethod
    def cosine_similarity(text1, text2):
        """
        :param text1, text2: list of tokens
        :return: float
        """
        try:
            tfidf = TfidfVectorizer().fit_transform(map(_SimilarityUtil._inverse, [text1, text2]))
            return 1 - cosine(tfidf[0].todense(), tfidf[1].todense())
        except ValueError:
            # Possible containing only stopwords
            return 0

if __name__ == '__main__':
    from Tokenizer import tokenize, tokenize_with_preprocess
    token1 = tokenize('I l\'ove reading')
    token2 = tokenize('I really love look book')
    print _SimilarityUtil.jaccard_similarity(token1, token2)

    token1_pre = tokenize_with_preprocess('I l\'ove reading')
    token2_pre = tokenize_with_preprocess('I really love look book')
    print _SimilarityUtil.jaccard_similarity(token1_pre, token2_pre)

    print _SimilarityUtil.cosine_similarity(token1_pre, token2_pre)
    print _SimilarityUtil.cosine_similarity(['love', 'apple'], ['love', 'apple'])
    print _SimilarityUtil.cosine_similarity(['a'], ['a'])
