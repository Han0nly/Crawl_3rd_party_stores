# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem



class CoolapkspiderSpider(CrawlSpider):
    name = 'coolapkspider'
    # allowed_domains = ['coolapk.com','101.71.72.158','113.200.91.143','113.200.91.141']
    # "https://coolapk.com/apk/tag/医疗"
    start_urls = ['https://coolapk.com/apk/tag/%E5%8C%BB%E7%96%97']

    rules = (
        Rule(LinkExtractor(allow=('https://coolapk.com/apk/tag/%E5%8C%BB%E7%96%97',)), follow=True,callback='parse_link'),
    )

    def parse_link(self,response):
        urls = response.xpath('//div[@id="game_left"]/div/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url='https://coolapk.com' + url, callback=self.parse_item)

    def parse_item(self,response):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        item["ID"] = "Coolapk_"+response.request.url.split('/')[-1]
        item["Name"] = response.xpath('//p[@class="detail_app_title"]/text()').extract_first()
        item["Version"] = response.xpath('//p[@class="detail_app_title"]/span/text()').extract_first().strip()
        item["Updated"] = response.xpath('//p[contains(text(),"详细信息")]/following-sibling::p[1]/text()[2]').extract_first().strip()[5:]
        item["Developer"] = response.xpath('//p[contains(text(),"详细信息")]/following-sibling::p[1]/text()[4]').extract_first().strip()[6:]
        # file_pipeline需要cookie
        # item["headers"] = response.headers[b'Set-Cookie']
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        item["file_urls"] = [response.xpath('/html/body/script[1]/text()').extract_first().split('"')[1]]
        item["file_type"] = '.apk'
        yield item
