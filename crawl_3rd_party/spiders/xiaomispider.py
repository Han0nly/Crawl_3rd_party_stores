# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem


class XiaomispiderSpider(CrawlSpider):
    name = 'xiaomispider'
    allowed_domains = ['mi.com','xiaomi.com']
    start_urls = []
    for i in range(0,67):
        url = 'http://app.mi.com/category/14#page='+str(i)
        start_urls.append(url)

    rules = (
        Rule(LinkExtractor(allow=('/category/14',)), follow=True),
        Rule(LinkExtractor(allow=("/details?", )), follow=False, callback='parse_link'),
    )

    def parse_start_url(self, response):
        self.parse_link(response)

    def parse_link(self,response):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        appid = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[10]/text()').extract_first()
        item["ID"] = "Xiaomi_"+response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[8]/text()').extract_first()
        item["Name"] = response.xpath('/html/body/div[6]/div[1]/div[2]/div[1]/div/h3/text()').extract_first()
        item["Version"] = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[4]/text()').extract_first()
        item["Updated"] = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[6]/text()').extract_first()
        item["Developer"] = response.xpath('/html/body/div[6]/div[1]/div[2]/div[1]/div/p[1]/text()').extract_first()
        # item["Market"] = "Xiaomi"
        # url = []
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        item["file_urls"] = ["http://app.mi.com/download/"+ appid]
        yield item
            # print(item)


