# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem


class QihuspiderSpider(Spider):
    name = 'qihuspider'
    allowed_domains = ['zhushou.360.cn']
    start_urls = []
    for i in range(1,105):
        start_urls.append('https://zhushou.360.cn/list/index/cid/15/'+str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102230/' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102231/' + str(i))

    # 医疗：https://zhushou.360.cn/list/index/cid/102233/
    # 新闻：https://zhushou.360.cn/list/index/cid/15/
    # 购物：https://zhushou.360.cn/list/index/cid/102230/
    # 旅游：https://zhushou.360.cn/list/index/cid/102231/



    def parse(self,response):
        if response.url.startswith('https://zhushou.360.cn/list/index/cid/15/'):
            category='360_新闻'
        elif response.url.startswith('https://zhushou.360.cn/list/index/cid/102230/'):
            category='360_购物'
        elif response.url.startswith('https://zhushou.360.cn/list/index/cid/102231/'):
            category='360_旅游'
        app_item = response.xpath('//ul[@id="iconList"]/li')
        if len(app_item) >= 1:
            # before
            for i in range(len(app_item)):
                item = Crawl3RdPartyItem()
                url = app_item[i].xpath('a[1]/@href').extract_first()
                # item['file_urls'] = []
                fullpath = app_item[i].xpath('a[2]/@href').extract_first()
                item['file_urls'] = [fullpath[fullpath.find('&url='):].strip('&url=')]
                # print("requesting:"+url )
                yield scrapy.Request(url='https://zhushou.360.cn' + url, meta={'key': item}, callback=self.parse_item,
                                     cb_kwargs=dict(category=category))

        # urls = response.xpath('//ul[@id="iconList"]/li/a[1]/@href').extract()

    def parse_item(self,response,category):
        # for title in response.xpath('/html'):
        item = response.meta['key']
        # appid = response.xpath('//div[@class="details preventDefault"]/ul[@class=" cf"]/li[10]/text()').extract_first()
        item["Name"] = response.xpath('//h2[@id="app-name"]/span[1]/text()').extract_first()
        item["Version"] = response.xpath('//strong[contains(text(),"版本：")]/../text()').extract_first()
        item["Updated"] = response.xpath('//strong[contains(text(),"更新时间：")]/../text()').extract_first()
        item["Developer"] = response.xpath('//strong[contains(text(),"作者：")]/../text()').extract_first()
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        # fullpath = response.xpath('//h2[@id="app-name"]/following-sibling::div[3]/a[1]/@href').extract_first()
        # extract direct download path
        # item["file_urls"] = [fullpath[fullpath.find('&url='):].strip('&url=')]
        item["ID"] = "360_"+item["file_urls"][0].split('/')[5].split('_')[0]
        item["file_type"] = '.apk'
        item["categories"] = category
        yield item
