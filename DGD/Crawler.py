# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import threading
from threading import Thread
import Queue
import time
import sys
import requests
import string

reload(sys)
sys.setdefaultencoding('utf-8')


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def add_pic_to_folder(alt, src):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'

    folder = 'wallhaven'  # 存放网页的文件夹
    filename = valid_filename(src)  # 将网址变成合法的文件名

    index = open(index_filename, 'a')
    index.write(alt + '\t' + filename.encode('ascii', 'ignore') + '\t' + src + '\n')
    index.close()

    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'wb')
    f.write(get_img(src))  # 将网页存入文件
    f.close()


def get_img(src):
    request = urllib2.Request(src)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    img = requests.get(src)
    return img.content


def get_page(page):
    try:
        request = urllib2.Request(page)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
        req = urllib2.urlopen(request,timeout=5).read()
        return req

    except:
        print "Fail to open your webpage"
        return ''


def get_crawl(seed):
    content = get_page(seed)
    soup = BeautifulSoup(content)
    preview = soup.findAll(class_= "preview")
    print len(preview)
    for i in preview:
        link = i.get("href")
        tocrawl.put(link)


def crawl():
    while not tocrawl.empty():
        page = tocrawl.get()
        if page not in crawled:

            print len(crawled), '\t', page

            if len(crawled) == MAX:
                return
            content = get_page(page)

            soup = BeautifulSoup(content)

            for i in soup.findAll(id="wallpaper"):
                alt = i.get("alt")
                print alt
                src = urlparse.urljoin(page, i.get("src"))
                print src
                add_pic_to_folder(alt, src)

            if varLock.acquire():
                crawled.append(page)
                varLock.release()
            tocrawl.task_done()


if __name__ == '__main__':
    MAX = 1000
    # start = time.clock()
    NUM = 20
    varLock = threading.Lock()
    crawled = []
    varLock = threading.Lock()
    tocrawl = Queue.Queue()

    seed = "https://alpha.wallhaven.cc/toplist?page="
    for j in range(2,10):
        get_crawl(seed+"{}".format(j))

    crawl()
    for i in range(NUM):
        globals()['t%s' % i] = Thread(target=crawl)
        globals()['t%s' % i].setDaemon(True)
        globals()['t%s' % i].start()

    for i in range(NUM):
        globals()['t%s' % i].join()
