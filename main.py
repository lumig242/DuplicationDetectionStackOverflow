import itertools
import numpy as np
import cPickle as pickle
import random
import warnings

from sklearn import linear_model
from Utils import *

# Do preprocessing for tokenize
tokenize = tokenize_with_preprocess


def _stripe_tag(tags):
    return sorted(tags.replace('&lt', '').replace('&gt;', ' ').split())


def preprocess(q_set):
    return {j['Id']: {'id': j['Id'],
                      'title': tokenize(j['Title']),
                      'body': tokenize(j['Body']),
                      'tags': _stripe_tag(j['Tags'])} for j in q_set}


def build_lda_model(train_set):
    lda = LDA([q['body'] for q in train_set.values()], n_topic=20)
    lda.print_topic_top_words(n_top_words=8)
    return lda


def build_feature(q1, q2, lda):
    """
    :param q1, q2: Pre-processed questions. A dict of all required attributes
    :param lda: Pre-trained lda model
    :return: A 4-d array of feature
    """
    # Title similarity
    x0 = SimilarityUtil.cosine_similarity(q1['title'], q2['title'])
    x1 = SimilarityUtil.cosine_similarity(q1['body'], q2['body'])
    x2 = SimilarityUtil.cosine_similarity(q1['tags'], q2['tags'])
    x3 = np.linalg.norm(lda.get_topic(q1['body']) - lda.get_topic(q2['body']))
    return np.array([x0, x1, x2, x3])


def prepare_train_data(all_questions, train_set, lda):
    X = []
    y = []
    for q in train_set:
        for dup in all_questions.get_dup(q):
            if dup in train_set:
                X.append(build_feature(train_set[q], train_set[dup], lda))
                y.append(1)
    print 'Generating random negative samples'
    # Generate negative samples as the same scale
    size_positive = len(y)
    q_set = train_set.keys()
    for _ in xrange(size_positive):
        q1 = random.choice(q_set)
        q2 = random.choice(q_set)
        X.append(build_feature(train_set[q1], train_set[q2], lda))
        y.append(0 if q2 not in all_questions.get_dup(q1) else 1)

    return np.array(X), np.array(y)


def prepare_validation_data(all_questions, train_set, test_set, lda):
    """
    :param all_questions:
    :param test_set:
    :param lda:
    :return: A tuple of four
     X_test_cross: feature matrix between newly found questions and old qustions
     y_test_cross: label array .................................................
     X_test_new:   feature matrix among newly found questions
     y_test_new:   label array ..............................
    """
    X_test_cross, y_test_cross = [], []
    X_test_new, y_test_new = [], []
    for q in test_set:
        for dup in all_questions.get_dup(q):
            if dup in test_set:
                # Among new questions
                X_test_new.append(build_feature(test_set[q], test_set[dup], lda))
                y_test_new.append(1)
            elif dup in train_set:
                X_test_cross.append(build_feature(test_set[q], train_set[dup], lda))
                y_test_cross.append(1)

    # Generate negative samples as the same scale
    print 'Generating random negative samples'
    size_positive_cross = len(y_test_cross)
    size_positive_new = len(y_test_new)
    q_set_train = train_set.keys()
    q_set_test = test_set.keys()

    for _ in xrange(20*size_positive_cross):
        q1 = random.choice(q_set_train)
        q2 = random.choice(q_set_test)
        X_test_cross.append(build_feature(train_set[q1], test_set[q2], lda))
        y_test_cross.append(0 if q2 not in all_questions.get_dup(q1) else 1)

    for _ in xrange(20*size_positive_new):
        q1 = random.choice(q_set_test)
        q2 = random.choice(q_set_test)
        X_test_new.append(build_feature(test_set[q1], test_set[q2], lda))
        y_test_new.append(0 if q2 not in all_questions.get_dup(q1) else 1)

    return tuple(map(np.array, (X_test_cross, y_test_cross, X_test_new, y_test_new)))


def load():
    warnings.filterwarnings("ignore")
    print "load all questions"
    # all_questions = QuestionSet('ec2-52-91-216-34.compute-1.amazonaws.com', 'root', '123456', 'pds_team')
    # with open('all_questions.pkl', 'wb') as f:
    #     pickle.dump(all_questions, f)
    with open('all_questions.pkl', 'rb') as f:
        all_questions = pickle.load(f)
    qids = all_questions.keys()
    random.shuffle(qids)
    split_size = int(len(qids) * 0.7)

    print "split train test sets"
    # train_set = preprocess(all_questions[qid] for qid in qids[:split_size])
    # test_set = preprocess(all_questions[qid] for qid in qids[split_size:])
    # with open('tmp.pkl', 'wb') as f:
    #     pickle.dump([train_set, test_set], f)

    print 'load data'
    with open('tmp.pkl', 'rb') as f:
        train_set, test_set = pickle.load(f)
    print 'build lda'
    #
    # lda = build_lda_model(train_set)
    # with open('lda.pkl', 'wb') as f:
    #     pickle.dump(lda, f)
    with open('lda.pkl', 'rb') as f:
        lda = pickle.load(f)

    # build_feature(train_set[0], train_set[1], lda)
    print 'loading training set'
    X_train, y_train = prepare_train_data(all_questions, train_set, lda)
    print 'loading test set'
    X_test_cross, y_test_cross, X_test_new, y_test_new = \
        prepare_validation_data(all_questions, train_set, test_set, lda)

    with open('final-data20.pkl', 'wb') as f:
        pickle.dump([X_train, y_train, X_test_cross, y_test_cross, X_test_new, y_test_new], f)


def main():
    # load()
    with open('final-data5.pkl', 'rb') as f:
        res = pickle.load(f)

    res = [np.nan_to_num(a) for a in res]

    X_train, y_train, X_test_cross, y_test_cross, X_test_new, y_test_new = res

    # Score
    logistic = linear_model.LogisticRegression(class_weight={0:1, 1:1})
    lr = logistic.fit(X_train, y_train)
    print logistic.coef_

    print len(y_train), len(y_test_cross), len(y_test_new)

    from sklearn.metrics import classification_report
    print classification_report(lr.predict(X_test_cross), y_test_cross)

    print classification_report(lr.predict(X_test_new), y_test_new)


if __name__ == '__main__':
    main()
