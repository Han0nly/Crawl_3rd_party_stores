# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem



class BaiduspiderSpider(CrawlSpider):
    name = 'baiduspider'
    allowed_domains = ['shouji.baidu.com']
    start_urls = ['https://shouji.baidu.com/software/504_board_100_018/']
    # 运动健身
    # https://shouji.baidu.com/software/504_board_100_019/

    rules = (
        Rule(LinkExtractor(allow=('https://shouji.baidu.com/software/504_board_100_019/',)), follow=False,callback='parse_link'),
        # Rule(LinkExtractor(allow=("/details?", )), follow=False, callback='parse_link'),
    )
    def parse_link(self, response):
        urls = response.xpath('//a[@class="app-box"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url='https://shouji.baidu.com' + url, callback=self.parse_item)

    def parse_item(self,response):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        # appid = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[10]/text()').extract_first()
        item["ID"] = "Baidu_"+response.xpath('//*[@id="doc"]/div[7]/div/div/div[5]/span/@data_package').extract_first()
        item["Name"] = response.xpath('//*[@id="doc"]/div[2]/div/div[1]/div/div[2]/h1/span/text()').extract_first()
        item["Version"] = response.xpath('//*[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[@class="version"]/text()').extract_first()[3:]
        item["Updated"] = []
        item["Developer"] = []
        # url = []
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        item["file_urls"] = [response.xpath('//*[@id="doc"]/div[2]/div/div[1]/div/div[4]/a/@href').extract_first()]
        yield item
