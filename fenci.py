#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append("../")
import jieba
from pymongo import *
import re,os

tagMap = {
	u'移动互联网': '1',
	u'电子商务': '2', 
	u'金融': '3', 
	u'企业服务': '4', 
	u'教育': '5', 
	u'文化娱乐': '6', 
	u'游戏': '7', 
	u'O2O': '8', 
	u'硬件': '9',
	u'医疗健康': '10', 
	u'生活服务': '11', 
	u'广告营销': '12', 
	u'旅游': '13', 
	u'数据服务': '14', 
	u'社交网络': '15', 
	u'分类信息': '16', 
	u'信息安全': '17', 
	u'招聘': '18', 
	u'其他': '19'
}

def get_db():
	client = MongoClient()
	db = client['result']
	return db

def get_col(db, col):
	col = db[col]
	return col

def get_content(cid):
	db = get_db()
	col = get_col(db, 'lagou')
	return col.find_one({'cid': cid})['content']

def get_doc(tag, number = -1):
    if os.path.isfile('./data/doc' + tagMap[tag] + '.txt'):
        doc = open('./data/doc' + tagMap[tag] + '.txt').read()
        return doc
    db = get_db()
    col = get_col(db, 'desdata')
    doc = ""
    item = col.find_one({'tag': tag})
    if number == -1:
    	for cid in item['content']:
    		doc += get_content(cid)
    else:
        for i in xrange(0, number):
            doc += get_content(item['content'][i])

    pattern = re.compile(r'www\..*?\.com');
    doc = pattern.sub("", doc)
    docfile = open('./data/doc' + tagMap[tag] + '.txt', 'w')
    docfile.write(doc)
    docfile.close()
    return doc

def stop_word(segs_list, tag):
    stopwords = [line.strip().decode('gb2312', 'ignore') for line in open('stopword.txt').readlines()]
    stopwords.append(tag)
    # for word in stopwords:
    #     print word.encode("gb2312", "ignore")
    final_list = []
    for seg in segs_list:
        if seg not in stopwords:
            final_list.append(seg)
    resultfile = open('./data/' + tagMap[tag] + '.txt', 'w');
    resultfile.write(' '.join(final_list))
    resultfile.close()



# for key in tagMap.keys():
# 	print key
# tag = '旅游'
# doc = get_doc(tag)
# segs = jieba.cut(doc.encode("gb2312", "ignore"))
# segs_list = list(segs)
# stop_word(segs_list, tag)
