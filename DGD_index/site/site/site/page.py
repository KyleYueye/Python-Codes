#!/usr/bin/env python
import os
import cv2
import tensorflow
import numpy as np
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import application.search.Search as text_search_server
import application.SIFT.SIFT_Search as sift_searcher
import application.label_extract as label_searcher
import application.TextSearch.Similarity_Search as tf_idf_searcher

define("port", default=8000, help="run on the given port", type=int)

# globals
print("load SIFT jsons")
with open(os.path.join(os.getcwd(), "application/SIFT", "sift_chars.json"),
          'r') as load_f:
    r_chars = json.load(load_f)
with open(os.path.join(os.getcwd(), "application/SIFT", "sift_files.json"),
          'r') as load_f:
    f_list = json.load(load_f)
with open(os.path.join(os.getcwd(), "application/SIFT", "hash_file.json"), "r") as f:
    file_list = json.load(f)
with open(os.path.join(os.getcwd(), "application/SIFT", "hash_hash.json"), "r") as f:
    hash_list = json.load(f)
print("load image text searcher")
detector = label_searcher.setModel('application')
dictionary, tfidf_vectors, file_list2 = tf_idf_searcher.load_models('application/TextSearch')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        random_item = text_search_server.random_three('index', 'newstxt')
        self.render('index.html', random_item=random_item)


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        mode = self.get_argument('mode')
        keyword = self.get_argument('keyword', '')
        page = int(self.get_argument('page', 1))
        total_count = self.get_argument('hits', None)
        alert_flag = False
        if total_count is None:
            total_count = text_search_server.total('index', keyword)
            alert_flag = True
        else:
            total_count = int(total_count)

        if mode == 'text-text':
            item_page = 10
            total_page = total_count // item_page + 1
            start = (page - 1) * item_page
            items = text_search_server.search('index', keyword, start, item_page)
            self.render('result.html',
                        items=items,
                        keyword=keyword,
                        mode=mode,
                        page=page,
                        count=total_count,
                        page_size=item_page,
                        total_page=total_page,
                        need_alert=alert_flag)
        elif mode == 'text-image':
            item_page = 12
            total_page = total_count // item_page + 1
            start = (page - 1) * item_page
            items = text_search_server.search('index', keyword, start, item_page)
            self.render('result_image.html',
                        items=items,
                        keyword=keyword,
                        mode=mode,
                        page=page,
                        count=total_count,
                        page_size=item_page,
                        total_page=total_page,
                        need_alert=alert_flag)


class SearchImageHandler(tornado.web.RequestHandler):
    def post(self):
        _img = self.request.files.get('image', None)
        if _img is None:
            self.redirect('/', permanent=True)
            return
        _img = bytearray(_img[0]['body'])
        _img = np.asarray(_img, dtype="uint8")
        img = cv2.imdecode(_img, cv2.IMREAD_GRAYSCALE)
        img_c = cv2.imdecode(_img, cv2.IMREAD_COLOR)

        # Img 4 Img
        print('search image by image')
        g_list = sift_searcher.search(img, r_chars, f_list, file_list, hash_list)
        img_items = []
        for g in g_list:
            t_res = text_search_server.get_by_imgpath('index', g)
            if t_res is not None:
                img_items.append(t_res)
        img_item = img_items[0]
        img_items = img_items[1:]

        # Img 4 TXT
        print('search text by image')
        str = label_searcher.label_extraction(img_c, detector)
        txt_items = text_search_server.search('index', str, 0, 10)
        self.render('image.html',
                    image_item=img_item,
                    image_items=img_items,
                    text_items=txt_items)


class ViewNewsHandler(tornado.web.RequestHandler):
    def get(self):
        handle = self.get_argument('handle', None)
        news = text_search_server.get_by_path('index', handle)
        res = tf_idf_searcher.TF_IDF(news['data']['contents'], dictionary, tfidf_vectors, file_list2)
        news_item = []
        for fname in res:
            news_item.append(text_search_server.get_by_path('index', fname))

        self.render('view.html',
                    news=news,
                    news_items=news_item)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "debug": True,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "template")
    }
    handlers = [
        (r"/", IndexHandler),
        (r"/s", SearchHandler),
        (r"/i", SearchImageHandler),
        (r"/v", ViewNewsHandler),
        (r"/(favicon.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))
    ]
    app = tornado.web.Application(handlers=handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
