#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-08 12:45:44
# Project: test
'''
@PhantomJS 是一个基于 WebKit 的服务器端 JavaScript API.
@这里借助pyspider框架，使用PhanomJs渲染异步加载的页面
@这段代码实现爬取36氪咨询首页的新闻列表内容
'''
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    def on_start(self):
        self.crawl('http://36kr.com/news',
                   fetch_type='js', callback=self.phantomjs_parser)

def phantomjs_parser(self, response):
    return [{
        "title": "".join(
            s for s in item('a').contents() if instance(s, basestring)
        ).strip(),
        "url": item('a').attr.href,
    } for item in response.doc('div.intro').items()]


