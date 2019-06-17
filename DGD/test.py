# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from threading import Thread
import re, sys, urllib2, jieba, urlparse, os, threading, Queue, time, requests, string,elasticsearch

reload(sys)
sys.setdefaultencoding('utf-8')



def date_time(str):
    return str[-16:-5],str[-5:]



def run():
    f = open("cont2.txt")
    content = f.read()
    soup = BeautifulSoup(content)
    title = soup.findAll(class_="news_title")[0].contents[0]  # title
    source = soup.findAll(class_="news_about")[0].contents[1].contents[0]
    date,time = date_time(soup.findAll(class_="news_about")[0].contents[3].contents[0])

    text = []
    for m in soup.findAll('br'):
        if not re.compile('^<').match(str(m.previousSibling)):
            text.append(' '.join(jieba.cut(m.previousSibling)))

    print title,'\n',source,'\n',date,' ',time,'\n'
    print text[0]
    # for i in text:
    #     print i
    f.close()

if __name__ == '__main__':
    run()