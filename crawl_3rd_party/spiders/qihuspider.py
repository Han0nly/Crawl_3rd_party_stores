# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem


class QihuspiderSpider(CrawlSpider):
    name = 'qihuspider'
    allowed_domains = ['zhushou.360.cn']
    start_urls = []
    for i in range(1,50):
        start_urls.append('https://zhushou.360.cn/list/index/cid/102233/?page='+str(i))

    rules = (
        Rule(LinkExtractor(allow=('https://zhushou.360.cn/list/index/cid/102233/?page=',)), follow=False, callback='parse_link'),
    )

    def parse_link(self,response):
        urls = response.xpath('//ul[@id="iconList"]/li/a[1]/@href').extract()
        for url in urls:
            yield scrapy.Request(url='https://zhushou.360.cn'+url,callback='parse_item')

    def parse_item(self,response):
        # for title in response.xpath('/html'):
        '/html/head/script[10]/text()'
        item = Crawl3RdPartyItem()
        # appid = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[10]/text()').extract_first()
        item["Name"] = response.xpath('//h2[@id="app-name"]/span[1]/text()').extract_first()
        item["Version"] = response.xpath('//strong[contains(text(),"版本：")]/../text()').extract_first()
        item["Updated"] = response.xpath('//strong[contains(text(),"更新时间：")]/../text()').extract_first()
        item["Developer"] = response.xpath('//strong[contains(text(),"作者：")]/../text()').extract_first()
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        fullpath = response.xpath('//h2[@id="app-name"]/following-sibling::div[2]/a[1]/@href').extract_first()
        # extract direct download path
        item["file_urls"] = fullpath[fullpath.find('&url='):].strip('&url=')
        item["ID"] = "360_"+item["file_urls"].split('/')[5].split('_')[0]
        yield item
