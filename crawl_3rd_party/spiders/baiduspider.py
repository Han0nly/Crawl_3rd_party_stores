# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem


class BaiduspiderSpider(CrawlSpider):
    name = 'baiduspider'
    allowed_domains = ['shouji.baidu.com']
    start_urls = ['https://shouji.baidu.com/software/']
    # 运动健身
    # https://shouji.baidu.com/software/504_board_100_019/
    # 购物：https://shouji.baidu.com/software/510_board_100_023/
    # 旅游：https://shouji.baidu.com/software/509/
    # 新闻：https://shouji.baidu.com/software/505_board_100_035/

    rules = (
        Rule(LinkExtractor(allow=(
        'software/501/', 'software/502/', 'software/503/', 'software/504/', 'software/505/', 'software/506/',
        'software/507/', 'software/508/', 'software/509/', 'software/510/',)), follow=True,
             callback='parse_link'),
        # Rule(LinkExtractor(allow=("/details?", )), follow=False, callback='parse_link'),
    )

    def parse_link(self, response):
        urls = response.xpath('//a[@class="app-box"]/@href').extract()
        category = response.xpath('//*[@id="doc"]/div[1]/span/text()').extract_first()
        for url in urls:
            yield scrapy.Request(url='https://shouji.baidu.com' + url, callback=self.parse_item,
                                 cb_kwargs=dict(category=category))

    def parse_item(self, response, category):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        # appid = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[10]/text()').extract_first()
        item["ID"] = "Baidu_" + response.xpath(
            '//*[@id="doc"]/div[7]/div/div/div[5]/span/@data_package').extract_first()
        item["Name"] = response.xpath('//*[@id="doc"]/div[2]/div/div[1]/div/div[2]/h1/span/text()').extract_first()
        item["Version"] = response.xpath(
            '//*[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[@class="version"]/text()').extract_first()[3:]
        item["Updated"] = []
        item["categories"] = "baidu_" + category
        item["Developer"] = []
        # url = []
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        item["file_urls"] = [response.xpath('//*[@id="doc"]/div[2]/div/div[1]/div/div[4]/a/@href').extract_first()]
        item["file_type"] = '.apk'
        item["file_type"] = response.xpath('//*[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[3]/text()').extract_first().split(':')[1].strip()
        item["app_url"] = response.request.url
        item["crawled_time"] = time.asctime(time.localtime(time.time()))
        yield item
