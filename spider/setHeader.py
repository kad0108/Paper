# coding=utf-8
'''
@本程序用来抓取受限网页(blog.csdn.net)
@User-Agent:客户端浏览器版本
@Host:服务器地址
@Referer:跳转地址
@GET:请求方法为GET
'''
import urllib2

url = "http://blog.csdn.net/FansUnion"

#定制自定义Header,模拟浏览器向服务器提交请求
csdn_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Host": "blog.csdn.net",
    'Referer': 'http://blog.csdn.net',
    "GET": url
    }
req = urllib2.Request(url,headers=csdn_headers)

#下载网页html并打印
html = urllib2.urlopen(req)
content = html.read()
print content
html.close()