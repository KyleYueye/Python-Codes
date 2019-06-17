from Index import ElasticObj


def create(name):
    obj = ElasticObj(name, name + "_type", ip="127.0.0.1")
    obj.create_index()
    obj.Index_Data("newstxt", "thepaper")


def replace(new):
    obj = ElasticObj(new, new + "_type", ip="127.0.0.1")
    obj.Delete(new)
    obj.create_index()
    obj.Index_Data("newstxt", "thepaper")


def delete(name):
    obj = ElasticObj(name, name + "_type", ip="127.0.0.1")
    ElasticObj.Delete(obj, name)


if __name__ == '__main__':
    create("index")
