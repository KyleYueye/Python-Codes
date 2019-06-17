# -*- coding: gbk -*-
# k = ln(2)*m/n
import time
from Bitarray import Bitarray
import random

k = 22
seeds = [13, 8]+[0]*(k-2)
for h in range(1, k):
    seeds[h] = (seeds[h-1]*seeds[h-2] % 12+6)*3


def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock() - start
    return run_time, result


def Hash(key,seed):
    # seed = 131 # 31 131 1313 13131 131313 etc..k
    hash = 0
    for i in range(len(key)):
        hash = (hash * seed) + ord(key[i])
    return hash


def make_hashtable(m):
    return Bitarray(m)


def hashtable_add(index, keyword):
    m = index.size
    for seed in seeds:
        index.set(Hash(keyword, seed) % m)


def get_random_string():
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 3))


def hashtable_lookup(index, keyword):
    m = index.size
    for seed in seeds:
        if not index.get(Hash(keyword, seed) % m):
            return False # Not recorded
        else:
            continue
    return True # Recorded


def actual_repeat(tocrawl):
    return len(tocrawl)-len(set(tocrawl))


def crawl_hashtable(tocrawl):
    repeat = 0
    table = make_hashtable(320000)
    while tocrawl:
        page = tocrawl.pop()
        if not hashtable_lookup(table,page):
            hashtable_add(table, page)
        else:
            repeat += 1
    return table,repeat


tocrawl = [get_random_string() for j in xrange(10**4)]


print (float(crawl_hashtable(tocrawl)[1]-actual_repeat(tocrawl))/10**4)


