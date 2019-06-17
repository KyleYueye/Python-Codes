import jieba.posseg as pseg
import codecs
from gensim import corpora, models, similarities
import json
import os

stop_words = os.path.join(os.getcwd(), 'application/TextSearch', 'stop_words.txt')
stopwords = codecs.open(stop_words, 'r', encoding='GB2312').readlines()
stopwords = [w.strip() for w in stopwords]

stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']


def tokenization(text):
    result = []
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result


def Corpus(filenames):
    corpus = []
    for each in filenames:
        corpus.append(tokenization(each))
    print(len(corpus))

    dictionary = corpora.Dictionary(corpus)
    print(dictionary)

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    print(len(doc_vectors))
    print(doc_vectors)

    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]

    print(len(tfidf_vectors))
    print(len(tfidf_vectors[0]))

    return dictionary, tfidf, tfidf_vectors, corpus


def TF_IDF(text, dictionary, tfidf_vectors, file_list, num=10):
    query = tokenization(text)
    query_bow = dictionary.doc2bow(query)

    # print(len(query_bow))
    # print(query_bow)

    index = similarities.MatrixSimilarity(tfidf_vectors)

    sims = index[query_bow]
    res = list(enumerate(sims))
    res = sorted(res, key=lambda elem: elem[1], reverse=True)
    # print(res)
    files = []
    for i in range(num):
        files.append(file_list[res[i][0]])
    return files


def LSI(file, dictionary, tfidf_vectors):
    lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=3)
    # lsi.print_topics(2)
    lsi_vector = lsi[tfidf_vectors]
    for vec in lsi_vector:
        print(vec)

    query = tokenization(file)
    query_bow = dictionary.doc2bow(query)
    print(query_bow)
    query_lsi = lsi[query_bow]
    print(query_lsi)

    index = similarities.MatrixSimilarity(lsi_vector)
    sims = index[query_lsi]
    print(list(enumerate(sims)))


def load_models(prefix=''):
    print("load TfidfModel")
    # tfidf = models.TfidfModel.load(
    #     os.path.join(os.getcwd(), prefix, "ths_tfidf.model")
    # )
    print("load Dictionary")
    dictionary = corpora.Dictionary.load(
        os.path.join(os.getcwd(), prefix, 'ths_dict.dict')
    )
    print("load corpus")
    with open(
            os.path.join(os.getcwd(), prefix, "corpus.json"), 'r'
    ) as load_f:
        corpus = json.load(load_f)
    print("load file list")
    with open(
            os.path.join(os.getcwd(), prefix, "file_list.json"), 'r'
    ) as load_f:
        file_list = json.load(load_f)

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    # print(len(doc_vectors))
    # print(doc_vectors)

    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    return dictionary, tfidf_vectors, file_list
