from Index import ElasticObj
import random,os


def keyword(name,key,start=0,size=10):
    """label = [title, imgpath, path, source, date, time, url]   """
    obj = ElasticObj(name,name+"_type",ip="127.0.0.1")
    return obj.Get_Data_By_Body("contents",key,start,size)[1]


def get_by_path(name,filename,start=0,size=10):
    obj = ElasticObj(name,name + "_type",ip="127.0.0.1")
    return obj.Get_Data_By_Body("path",filename,start,size)[1][0]


def get_by_imgpath(name,filename,start=0,size=10):
    obj = ElasticObj(name,name + "_type",ip="127.0.0.1")
    return obj.Get_Data_By_Body("imgpath",filename,start,size)[1][0]


def random_three(root,name):
    result = []
    for m,dirnames,filenames in os.walk(root):
        MAX = len(filenames)
        for i in range(3):
            ran = random.randint(0,MAX)
            # print(filenames[ran])
            result.append(get_by_path(name, root+"\\"+filenames[ran]))
    return result


if __name__ == '__main__':
    # print(get_by_imgpath("a2","thepaper1\\httpsimage2.thepaper.cnimage1469993.jpg",0,6))
    # print(keyword("a2","国足",0,6))
    print(random_three("newstxt1","a2")[1])
