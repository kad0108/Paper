#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 受代理的http请求数限制，加载慢，需要进一步做判断处理


from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time  
from selenium.webdriver.common.proxy import *

from pymongo import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 'proxy': 'HWJB1R49VGL78Q3D:0C29FFF1CB8308C4@proxy.abuyun.com:9020'
myProxy= 'proxy.abuyun.com:9020'



option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=C:\Users\zml\AppData\Local\Google\Chrome\User Data\Default') #设置成用户自己的数据目录
option.add_argument('--proxy-server=%s' % myProxy)


browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=option)

browser.get("https://www.baidu.com") # Load page
time.sleep(10)



client = MongoClient()
db = client['result']
col = db['lagou']
encodeName = "gb18030"


def getContent(cid, browser):
    print cid
    time.sleep(4)
    url = "https://www.lagou.com/gongsi/" + str(cid) + ".html"
    browser.get(url)

    try:
        browser.find_element_by_class_name("text_over").click()
    except Exception, e:
        pass

    soup = BeautifulSoup(browser.page_source, "html.parser")

    total = 0
    for item in soup.select('#company_navs li'):
        tmp = item.find('a').text.encode(encodeName, "ignore")
        if tmp.find(u'招聘职位'.encode(encodeName, "ignore")) != -1:
            total = int(tmp[10:len(tmp)-2])
    if total != 0:
        name = soup.select(".company_main > h1 > a")[0].text.encode(encodeName, "ignore")
        info = soup.select('#basic_container ul > li')
        tag = info[0].find('span').text.encode(encodeName, "ignore")
        process = info[1].find('span').text.encode(encodeName, "ignore")
        cont = ""
        for ele in soup.select(".company_intro_text > .company_content > p"):
            cont += ele.text.encode(encodeName, "ignore")
        if cont == "":
            cont = soup.select(".company_intro_text > .company_content").text.encode(encodeName, "ignore")
        obj = {
            "cid": cid,
            "url": url.decode(encodeName).encode("utf-8"),
            "name": name.decode(encodeName).encode("utf-8"),
            "content": cont.decode(encodeName).encode("utf-8"),
            "tag": tag.decode(encodeName).encode("utf-8"),
            "process": process.decode(encodeName).encode("utf-8"),
            "salary": [],
            "total": total
        }
        col.insert(obj)
        getPosition(cid, browser)


def getPosition(cid, browser):
    print cid
    pageNo = 1
    time.sleep(4)
    url = "https://www.lagou.com/gongsi/j" + str(cid) + ".html"
    browser.get(url)


    soup = BeautifulSoup(browser.page_source, "html.parser")
    if col.find_one({'cid': cid})['total'] <= 10:
        for ele in soup.select(".con_list_item > .item_detail > .item_salary"):
            col.update({"cid": cid}, {"$push": {"salary": (ele.text).encode(encodeName, "ignore")}})
        return

    #等待分页数据加载
    while 1:
        for ele in soup.select(".con_list_item > .item_detail > .item_salary"):
            col.update({"cid": cid}, {"$push": {"salary": (ele.text).encode(encodeName, "ignore")}})

        tag = soup.select(".next")[0]
        if len(tag['class']) == 2: # contain u'next', u'disable'
            break;

        browser.find_element_by_class_name("next").click()
        time.sleep(4)
        pageNo += 1
        while 1:
            soup = BeautifulSoup(browser.page_source, "html.parser")

            newPage = soup.select('.pages > .current')[0].text.encode(encodeName, "ignore")
            newPage = int(newPage)
            print "New page number:", newPage, "; real page:", pageNo
            if newPage and pageNo == newPage:
                break
            else:
                time.sleep(1)
        #soup = BeautifulSoup(browser.page_source, "html.parser")


for cid in range(22708, 22711):
    getContent(cid, browser)