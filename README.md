# Paper

## Reference

[Pyspider获取json数据](https://segmentfault.com/a/1190000002477870)

[Pyspider + PhantomJS渲染动态页面](https://segmentfault.com/a/1190000002477913)

[MongoDB：NoSQL](http://www.runoob.com/mongodb/mongodb-tutorial.html)

* 启动MongoDB
```
cd到mongo安装文件夹的bin目录下
mongod.exe --dbpath D:\software\mongo
用--dbpath指定数据存放地点为mongo文件夹
```

* 连接MongoDB
```
cd到bin目录下
mongo
```

* 可视化工具Robomongo

[PyMongo：python操作MongoDB的模块](https://api.mongodb.com/python/current/tutorial.html)

Wappalyzer: 分析网站使用了哪些技术和工具

[LDA 文本分析 实验样例](https://www.zhihu.com/question/39254526?q=%E5%81%9A%E6%96%87%E6%9C%AC%E5%88%86%E6%9E%90%E5%A6%82%E4%BD%95%E6%89%BE%E5%A5%BD%E7%9A%84%E8%AF%AD%E6%96%99)

LDA代码：[代码一](https://github.com/a55509432/python-LDA)，[代码二](https://github.com/yimiwawa/pyLDA)

[Selenium 中文文档](http://selenium-python-zh.readthedocs.io/en/latest/getting-started.html)

[BeautifulSoup 中文文档](http://beautifulsoup.readthedocs.io/zh_CN/latest/#id41)



## 爬取动态网页

* 静态爬虫借助python中的urllib和beautifulsoup很容易实现
* 抓包分析：NetWork中获取json请求地址，抓取速度快
* 驱动浏览器内核：占用资源多，慢
* 动态爬虫工具（调用浏览器内核解析页面）：
  1. selenium + webdriver  有界面浏览器
  2. headless phantomjs 速度比前者快



## IP被封，解决办法：

* 降低爬取频率
* 更换user-Agent，模拟不同浏览器
* 使用高匿代理，隐藏客户真实ip
* ip解封后用phantomjs就拿不到json数据了，所以改用selenium去驱动真实浏览器渲染页面然后再去爬取

