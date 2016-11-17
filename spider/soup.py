# coding=utf-8
'''
@安装beautifulsoup4，一个可以从HTML或XML文件中提取数据的Python库。
使用过程中遇到问题，网页内容是通过ajax异步加载进来的，所以爬到的文部分是空标签。
'''
import urllib2
from bs4 import BeautifulSoup

url = "http://36kr.com/p/5055725.html"
# 下载网页
csdn_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Host": "36kr.com",
    "GET": url
    }
req = urllib2.Request(url,headers=csdn_headers)

html = urllib2.urlopen(req)
content = html.read()
print content
html.close()

# 使用BeautifulSoup匹配图片
html_soup = BeautifulSoup(content, "html.parser")
# 相较通过正则表达式去匹配,BeautifulSoup提供了一个更简单灵活的方式
ans = html_soup.findAll('section', class_='summary')
print ans

