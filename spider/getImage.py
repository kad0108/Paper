#coding=utf-8
import urllib
import re

# 获取网页html信息
url = "http://tieba.baidu.com/p/2336739808"
html = urllib.urlopen(url)
content = html.read()
html.close()

# 通过正则匹配图片特征,并获取图片链接
img_tag = re.compile(r'class="BDE_Image" src="(.+?\.jpg)"')
img_links = re.findall(img_tag, content)
print img_links

# 下载图片 img_counter为图片计数器(文件名)
img_counter = 0
for img_link in img_links:
    img_name = '%s.jpg' % img_counter
    urllib.urlretrieve(img_link, "\\Users\\zml\\Desktop\\2016-11\\file\\%s" %img_name)#数据保存到本地
    img_counter += 1