# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem
import time
import json


class QqspiderSpider(CrawlSpider):
    name = 'qqspider'
    # allowed_domains = ['sj.qq.com']
    start_urls = ['https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=109&pageSize=40&pageContext=0']

    rules = (
        Rule(LinkExtractor(allow=(r'/myapp/cate/appList.htm', )), follow=False, callback='parse_link'),
    )
    # rules = (
    #     Rule(LinkExtractor(allow=('https://apkpure.com/medical\?page=',)), follow=True, callback='parse_link'),
    # )
    def parse_start_url(self, response):
        return self.parse_link(response)

    def parse_link(self, response):
        print("asdaaaaaaaaaaaaaaaaaaaaa")
        json_dict = json.loads(response.text)
        if(json_dict['obj']):
            for obj in json_dict['obj']:
                item = Crawl3RdPartyItem()
                item["ID"] = "QQ_"+obj['pkgName']
                item["Name"] = obj['appName']
                item["Version"] = obj['versionName']
                item["Updated"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(obj['apkPublishTime']))
                item["Developer"] = obj['authorName']
                item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
                item["file_urls"] = [obj['apkUrl']]
                yield item
            if(json_dict['pageContext']):
                yield scrapy.Request(url="https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=109&pageSize=20&pageContext="+json_dict['pageContext'],callback=self.parse_link)
        else:
            yield response.request


