import os
from os import walk
import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def date_time(str):
    str = str.strip()
    mh = str.index(':')
    line = str.index('-')
    time = str[mh - 2:mh + 3]
    date = str[line - 4:line + 6]
    return date, time

def geturl(filename):
    f = open("index.txt",'r')
    for i in f.readlines():
        name,url = i.split('\t')
        url = url.strip()
        if filename == name:
            return url

def find_img(filename, folder):
    """ewyruqew.jpg    wydgfwuyf.jpeg   wgyufgewfu.png  reger.gif"""

    if os.path.exists(os.path.join(folder, filename[:-4] + ".jpg")):
        return os.path.join(folder, filename[:-4] + ".jpg")
    if os.path.exists(os.path.join(folder, filename[:-4] + "jpeg")):
        return os.path.join(folder, filename[:-4] + "jpeg")
    if os.path.exists(os.path.join(folder, filename[:-4] + ".png")):
        return os.path.join(folder, filename[:-4] + ".png")
    if os.path.exists(os.path.join(folder, filename[:-4] + ".gif")):
        return os.path.join(folder, filename[:-4] + ".gif")
    return "No_img"


class ElasticObj:
    def __init__(self, index_name, index_type, ip="127.0.0.1"):
        '''
        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        # self.es = Elasticsearch([ip])
        # 用户名密码状态
        self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)

    def create_index(self, index_name="ott", index_type="ott_type"):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        # 创建映射
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "title": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "contents": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "date": {
                            "type": "date",
                            "index": True
                        },
                        "time": {
                            "type": "keyword",
                            "index": True
                        },
                        "source": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "path": {
                            "type": "keyword",
                            "index": True
                        },
                        "imgpath": {
                            "type": "keyword",
                            "index": True
                        },
                        "url": {
                            "type": "text",
                            "index": True
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            print(res)

    def Delete(self, name):
        self.es.indices.delete(index=name)

    def Index_Data(self, root, img):
        '''
        数据存储到es
        :return:
        '''

        list = []
        count = 0
        for root, dirnames, filenames in walk(root):
            for filename in filenames:
                count += 1

                tmp = {}
                print(count, " adding index:", filename)
                # if not filename.endswith('.txt'):
                #     continue
                path = os.path.join(root, filename)
                with open(path, encoding='utf8') as file:
                    contents = file.read()
                file.close()

                file = open(path, encoding='utf8')
                lines = file.readlines()
                title = lines[0]

                source = lines[1]
                if not source:
                    source = "No_source"

                date, time = date_time(lines[2])
                tmp["date"] = date.strip()
                tmp["time"] = time.strip()
                tmp["title"] = title
                tmp["source"] = source
                tmp["path"] = path
                tmp["contents"] = contents
                tmp["imgpath"] = find_img(filename, img)
                tmp["url"] = geturl(filename)
                print(date, time, source, '\n', title, path, '\n')

                list.append(tmp)

        for item in list:
            res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            print(res['result'])

    def Get_Data_By_Body(self, label, keyword, start=0, size=10):
        # doc = {'query': {'match_all': {}}}
        doc = {
            "query": {
                "match": {
                    label: keyword
                },

            },
            "highlight": {
                "pre_tags": ['<span style="color:red">'],
                "post_tags": ["</span>"],
                "fields": {
                    label: {}
                }
            },
            "from": start,
            "size": size
        }
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)

        total_result = _searched['hits']['total']
        print("{} results found\n".format(total_result))

        result = []

        for hit in _searched['hits']['hits']:
            result.append({'data': hit['_source'],
                           'score': hit['_score'],
                           'highlight': hit["highlight"]})
        return total_result, result


if __name__ == '__main__':
    obj = ElasticObj("index5", "index5_type", ip="127.0.0.1")

    # obj = ElasticObj("ott1", "ott_type1")

    obj.create_index()

    obj.Index_Data("newstxt", "thepaper")

    # obj.Delete_Index_Data(1)

    # obj.Get_Data_By_Body("title",input("keyword:"),int(input("num:")))
