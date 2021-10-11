# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem


class QihuspiderSpider(Spider):
    name = 'qihuoldspider'
    allowed_domains = ['zhushou.360.cn']
    start_urls = []
    for i in range(1,105):
        start_urls.append('https://zhushou.360.cn/list/index/cid/11/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/12/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/14/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/15/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/16/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/18/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/17/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102228/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102230/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102231/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102232/1?page=' + str(i))
        start_urls.append('https://zhushou.360.cn/list/index/cid/102233/1?page=' + str(i))
    # rules = (
    #     Rule(LinkExtractor(allow=(r'/detail/index/soft_id/', )), follow=True, callback='parse_link'),
    # )
    # 医疗：https://zhushou.360.cn/list/index/cid/102233/
    # 新闻：https://zhushou.360.cn/list/index/cid/15/
    # 购物：https://zhushou.360.cn/list/index/cid/102230/
    # 旅游：https://zhushou.360.cn/list/index/cid/102231/

    def parse(self, response, **kwargs):
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
                yield scrapy.Request(url='https://zhushou.360.cn' + url, meta={'key': item}, callback=self.parse_item)

        # urls = response.xpath('//ul[@id="iconList"]/li/a[1]/@href').extract()

    def parse_item(self,response):
        # for title in response.xpath('/html'):
        item = response.meta['key']
        if response.xpath('/html/head/title/text()').extract_first() == '错误提示':
            return None
        # info = response.xpath('/html/head/script[10]/text()').extract_first()
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
        tags = response.xpath("/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]/a/text()").extract()
        item["categories"] = tags
        item["installs"] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div[1]/span[3]/text()').extract_first()[3:]
        yield item
