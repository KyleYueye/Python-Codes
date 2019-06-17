# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from threading import Thread
import re, sys, urllib2, jieba, urlparse, os, threading, Queue,requests, string
reload(sys)
sys.setdefaultencoding('utf-8')


def date_time(str):
    try:
        str = str.strip()
        mh = str.index(':')
        line = str.index('-')
        time = str[mh - 2:mh + 3]
        date = str[line - 4:line + 6]
        return date,time
    except:
        return str[-16:-5],str[-5:]


def geturl(filename):
    f = open("index.txt",'r')
    for i in f.readlines():
        name,url = i.split('\t')
        url = url.strip()
        if filename == name:
            return url

def run():
    folder = "newstxt1"
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)

    root = "newscontent1"
    count = 1
    for root,dirnames,filenames in os.walk(root):
        for filename in filenames:
            print count,filename
            count += 1
            if os.path.exists(os.path.join(folder,filename)):
                continue
            path = os.path.join(root,filename)
            file = open(path)
            content = file.read()
            file.close()
            soup = BeautifulSoup(content)
            url = geturl(filename)
            try:
                title = soup.findAll(class_="news_title")[0].contents[0]  # title
            except:
                continue
            try:
                source = soup.findAll(class_="news_about")[0].contents[1].contents[0]
            except:
                source = "No_source"
            date,time = date_time(soup.findAll(class_="news_about")[0].contents[3].contents[0])
            newfile = open(os.path.join(folder,filename),'w')
            newfile.write(title + '\n' + source + '\n' + date + '\t' + time + '\n')
            for m in soup.findAll('br'):
                if not re.compile('^<').match(str(m.previousSibling)):
                    newfile.write(str(m.previousSibling) + '\n')


if __name__ == '__main__':
    run()
