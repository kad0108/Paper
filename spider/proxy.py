from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'proxy': 'HWJB1R49VGL78Q3D:0C29FFF1CB8308C4@proxy.abuyun.com:9020'
    }
    def on_start(self):
        self.crawl("http://httpbin.org/ip", callback=self.test_page)
    
    def test_page(self, response):
        print response.json