#coding=utf-8
'''
Pymongo是python操作MongoDB的模块，先启动mongodb再建立连接
'''
from pyspider.libs.base_handler import *
from pymongo import *

client = MongoClient()#建立连接
db = client['result']#拿到数据库result
col = db['kr']#拿到集合kr
class Handler(BaseHandler):
    def on_start(self):
        self.crawl('http://36kr.com/p/5056145.html',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'},fetch_type='js', callback=self.phantomjs_parser)
    def phantomjs_parser(self, response):
        res_list = []
        for item in response.doc('div.mainlib').items():
            obj = {
                "title": item('h1').text(),
                "content": item('section.textblock').text()
            }
            col.insert(obj)
            res_list.append(obj)
        return res_list