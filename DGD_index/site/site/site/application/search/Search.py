from application.search.Index import ElasticObj
import random
import os


def keyword(name, key, start=0, size=10):
    """label = [title, imgpath, path, source, date, time]   """
    obj = ElasticObj(name, name + "_type", ip="127.0.0.1")
    return obj.Get_Data_By_Body("contents", key, start, size)


def get_by_path(name, filename, start=0, size=1):
    obj = ElasticObj(name, name + "_type", ip="127.0.0.1")
    c, r = obj.Get_Data_By_Body("path", filename, start, size)
    if c != 0:
        return r[0]
    else:
        return None


def get_by_imgpath(name, filename, start=0, size=1):
    obj = ElasticObj(name, name + "_type", ip="127.0.0.1")
    c, r = obj.Get_Data_By_Body("imgpath", filename, start, size)
    if c != 0:
        return r[0]
    else:
        return None


def total(name, key):
    return keyword(name, key)[0]


def search(name, key, start=0, size=10):
    return keyword(name, key, start, size)[1]


def random_three(name, root):
    result = []
    for _, dirnames, filenames in os.walk(os.path.join(os.getcwd(), "application/search", root)):
        MAX = len(os.path.join(os.getcwd(), "application/search", root))
        for i in range(3):
            ran = random.randint(0, MAX)
            result.append(get_by_path(name, root + '/' + filenames[ran]))
    return result


if __name__ == '__main__':
    for i in keyword("index", "国足", 0, 10)[1]:
        print(i['score'], i['data']['title'])
