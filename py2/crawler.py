# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import threading
import Queue
import time
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')




def get_page(page):
    try:
        r = requests.get(page, timeout=5)
        req = urllib2.urlopen(page).read()
        return req
    except:
        print "Fail to open your webpage"
        return ''


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content)
    for i in soup.findAll('a',{'href':re.compile('^http|^/')}):
        if str(i.get('href',''))[0] == '/':
            links.append(urlparse.urljoin(page,i.get('href','')))
        else:
            links.append(i.get('href',''))
    return links


def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)


def union_bfs(a,b):
    for e in b:
        if e not in a:
            a.insert(0,e)


def crawl():
    while not tocrawl.empty():
        page = tocrawl.get()
        if page not in crawled:
            print len(crawled),'\t',page

            if len(crawled) == MAX: return

            content = get_page(page)
            outlinks = get_all_links(content, page)
            if len(crawled) < 3:
                for link in outlinks:
                    tocrawl.put(link)
            if varLock.acquire():
                crawled.append(page)
                graph[page] = outlinks
                varLock.release()
            tocrawl.task_done()



if __name__ == '__main__':
    MAX = int(sys.argv[1])
    start = time.clock()
    NUM = 2
    varLock = threading.Lock()
    crawled = []
    graph = {}
    tocrawl = Queue.Queue()
    # seed = "http://www.baidu.com/"
    seed = sys.argv[2]
    tocrawl.put(seed)
    thread1 = threading.Thread(target=crawl)
    thread1.setDaemon(True)
    thread1.start()
    thread2 = threading.Thread(target=crawl)
    thread2.setDaemon(True)
    thread2.start()
    thread1.join()
    thread2.join()
    end = time.clock()

    print end-start
