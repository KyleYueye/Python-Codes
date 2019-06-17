import jieba.posseg as pseg
import codecs
from gensim import corpora, models, similarities
import json
import os

stop_words = 'stop_words.txt'
stopwords = codecs.open(stop_words, 'r', encoding='GB2312').readlines()
stopwords = [w.strip() for w in stopwords]

stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']


def tokenization(filename):
    result = []
    with open(filename, 'r') as f:
        text = f.read()
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


def TF_IDF(file, dictionary, tfidf_vectors):
    query = tokenization(file)
    query_bow = dictionary.doc2bow(query)

    print(len(query_bow))
    print(query_bow)

    index = similarities.MatrixSimilarity(tfidf_vectors)

    sims = index[query_bow]
    res = list(enumerate(sims))
    print(res)
    return res


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


def preprocess(filenames):
    dictionary, tfidf, tfidf_vectors, corpus = Corpus(filenames)
    # file = "texts/1.txt"
    # LSI(file,dictionary,tfidf_vectors)
    dictionary.save('ths_dict.dict')  # 保存生成的词典
    # corpora.MmCorpus.serialize('ths_corpuse.mm', corpus)  # 将生成的语料保存成MM文件
    tfidf.save("ths_tfidf.model")  # 保存成model格式
    with open("corpus.json", "w") as f:
        json.dump(corpus, f)
    with open("file_list.json","w") as f:
        json.dump(filenames,f)


if __name__ == '__main__':
    dir = "newstxt"
    files = os.listdir(dir)
    file_list = []
    for file in files:
        file_list.append(dir + '/' + file)
    preprocess(file_list)
