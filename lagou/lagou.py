#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-22 11:56:47
# Project: newproxy
from pyspider.libs.base_handler import *
from pymongo import *
import random
import time
client = MongoClient()
db = client['result']
col = db['lagou']
class Handler(BaseHandler):
    crawl_config = {
        'proxy': 'HWJB1R49VGL78Q3D:0C29FFF1CB8308C4@proxy.abuyun.com:9020'
    }
    def on_start(self):
        #self.crawl('http://httpbin.org/ip', callback=self.test_page)
        self.run(90867, -1)
        
    def test_page(self, response):
        print response.json
    def index_page(self, response):
        companyId = response.save['companyId']
        content = response.doc('.company_intro_text>.company_content>p').text()
        info = response.doc('#basic_container ul>li').items()
        try:
           tag = info.next()('span').text()
        except StopIteration:
            tag = ''
        
        try: 
            process = info.next()('span').text()
        except StopIteration:
            process = ''
            
        obj = {
            "companyId": companyId,
            "url": response.url,
            "name": response.doc(".company_main>h1>a").text(),
            "content": content,
            "tag": tag,
            "process": process,
            "salary": []
        }
        col.insert(obj)
        self.run(companyId, 1)
   
    
    def json_parser(self, response):
        companyId = response.save['companyId']
        print response.text
        page = response.json['content']['data']['page']
        pageNo = int(page['pageNo'])
        total = int(page['totalCount'])
        
        if total/10 == 0:
            totalPageSize = total/10
        else :
            totalPageSize = total/10 + 1
        
        
        col.update({"companyId": companyId},{"$set":{"total":total}})
        
        for x in page['result']:
            col.update({"companyId": companyId}, {"$push": {"salary": x['salary']}})
            
        print pageNo,totalPageSize
        if pageNo < totalPageSize: 
            pageNo += 1
            self.run(companyId, pageNo)
            
            
            
    def getAgent(self):
        file_object = open('C:\\Users\\zml\\Desktop\\agents.py')
        try:
            all_the_text = file_object.read( )
            ans_tmp = all_the_text.split("\",")
            ans =[]
            for x in ans_tmp:
                if x.strip() == "": continue
                beg = 0
                end = len(x)
                while beg < end and (x[beg] == '\"' or x[beg] == '\n'):
                    beg+=1
                while beg < end and (x[end-1] == '\"' or x[end-1] == '\n'):
                    end-=1
                ans.append(x[beg:end])
            rad = int(random.random() * len(ans))
            agent = ans[rad]
        finally:
            file_object.close( )
        return agent
    
    def run(self, cid, pageNo):
        agent = self.getAgent()
        try:
            time.sleep(3)
            if pageNo == -1:
                self.crawl('https://www.lagou.com/gongsi/'+ str(cid) + '.html',headers={'User-Agent': agent}, js_script="""function(){setTimeout("$('.text_over').click()", 1000);}""",  callback=self.index_page, save={'companyId': cid}, validate_cert=False)
            else:
                self.crawl('https://www.lagou.com/gongsi/searchPosition.json?companyId=' + str(cid) + '&pageNo=' + str(pageNo), headers={'User-Agent': agent}, save={'companyId': cid}, callback=self.json_parser, validate_cert=False)
        except Exception, e:
            print e 