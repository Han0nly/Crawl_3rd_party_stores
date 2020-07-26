# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem



class CoolapkspiderSpider(CrawlSpider):
    name = 'coolapkspider'
    # allowed_domains = ['coolapk.com','101.71.72.158','113.200.91.143','113.200.91.141']
    # 医疗：https://coolapk.com/apk/tag/医疗
    # 购物：https://coolapk.com/apk/shopping/?p=1
    # 新闻：https://coolapk.com/apk/news
    # 旅游：https://coolapk.com/apk/trave
    start_urls = ['https://coolapk.com/apk/shopping/?p=1','https://coolapk.com/apk/news','https://coolapk.com/apk/trave']

    rules = (
        Rule(LinkExtractor(allow=('https://coolapk.com/apk/shopping/',)), follow=True,callback='parse_link'),
        Rule(LinkExtractor(allow=('https://coolapk.com/apk/news',)), follow=True, callback='parse_link'),
        Rule(LinkExtractor(allow=('https://coolapk.com/apk/trave',)), follow=True, callback='parse_link'),
    )

    def parse_link(self,response):
        urls = response.xpath('//div[@id="game_left"]/div/a/@href').extract()
        if response.url.startswith('https://coolapk.com/apk/news'):
            category = 'CoolAPK_新闻'
        elif response.url.startswith('https://coolapk.com/apk/shopping'):
            category = 'CoolAPK_购物'
        elif response.url.startswith('https://coolapk.com/apk/trave'):
            category = 'CoolAPK_旅游'
        for url in urls:
            yield scrapy.Request(url='https://coolapk.com' + url, callback=self.parse_item,cb_kwargs=dict(category=category))

    def parse_item(self,response,category):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        item["ID"] = "Coolapk_"+response.request.url.split('/')[-1]
        item["Name"] = response.xpath('//p[@class="detail_app_title"]/text()').extract_first()
        item["Version"] = response.xpath('//p[@class="detail_app_title"]/span/text()').extract_first().strip()
        item["Updated"] = response.xpath('//p[contains(text(),"详细信息")]/following-sibling::p[1]/text()[2]').extract_first().strip()[5:]
        item["Developer"] = response.xpath('//p[contains(text(),"详细信息")]/following-sibling::p[1]/text()[4]').extract_first().strip()[6:]
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        item["categories"] = category
        item["file_urls"] = [response.xpath('/html/body/script[1]/text()').extract_first().split('"')[1]]
        item["file_type"] = '.apk'
        yield item
