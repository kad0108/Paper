#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import *
import crawlLagou

client = MongoClient()
db = client['result']
col = db['lagou']

encodeName = "gb18030"


def isValidCompanyInfo(companyInfo):
	if companyInfo['cid'] == -1: return False
	if companyInfo['name'] == crawlLagou.Page404Name or\
		companyInfo['name'] == crawlLagou.PageStillConstructionName:
		return False
	return True

def storage():
	for cid in xrange(22708, 100000):
	# for cid in xrange(23622, 23622+1):
		infoObj = col.find_one({"cid": cid})
		if infoObj == None:
			info = crawlLagou.getCompanyInfo(cid) # return dict
			if info['cid'] != -1:
				info = mongoEncoding(info)
				col.insert(info)
				if isValidCompanyInfo(info) and info['total'] != 0:
					jobinfo = crawlLagou.getCompanyJobsInfoFromJson(cid)
					for arrItem in jobinfo:						
						arrItem = mongoEncoding(arrItem)
						col.update({"cid": cid}, {"$push": {"salary": arrItem['salary']}})

		elif isValidCompanyInfo(infoObj) and infoObj['total'] != 0 and infoObj['total'] != "":
			if len(infoObj['salary']) == 0 or len(infoObj['salary']) != infoObj['total']:
				jobinfo = crawlLagou.getCompanyJobsInfoFromJson(cid)
				col.update({"cid": cid}, {"$set": {"salary": []}})
				col.update({"cid": cid}, {"$set": {"total": len(jobinfo)}})
				for arrItem in jobinfo:
					arrItem = mongoEncoding(arrItem)
					salary = arrItem['salary']
					col.update({"cid": cid}, {"$push": {"salary": salary }})

def mongoEncoding(obj):
	for item in obj:
		if isinstance(obj[item], str):
			obj[item] = obj[item].decode(encodeName).encode("utf-8")
	return obj

storage()