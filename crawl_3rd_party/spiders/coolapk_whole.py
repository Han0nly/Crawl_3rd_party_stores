# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem


class CoolapkWholeSpider(CrawlSpider):
    name = 'coolapkwholespider'
    allowed_domains = ['coolapk.com', '101.71.72.158', '113.200.91.143', '113.200.91.141']
    start_urls = ['https://coolapk.com/apk']

    rules = (
        Rule(LinkExtractor(allow=(
        '/apk/shopping', '/apk/news', '/apk/trave', '/apk/system', '/apk/desktop', '/apk/themes', '/apk/sns',
        '/apk/network', '/apk/media', '/apk/photography', '/apk/life', '/apk/tools', '/apk/business', '/apk/finance',
        '/apk/sport', '/apk/education', '/apk/xposed', '/apk/vr', '/apk/other')), follow=True, callback='parse_link'),
    )

    def parse_link(self, response):
        urls = response.xpath('//div[@id="game_left"]/div/a/@href').extract()
        category = response.xpath('//*[@id="game_left"]/div/div[1]/span/text()').extract_first()
        for url in urls:
            yield scrapy.Request(url='https://coolapk.com' + url, callback=self.parse_item,
                                 cb_kwargs=dict(category=category))

    def parse_item(self, response, category):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        item["ID"] = "Coolapk_" + response.request.url.split('/')[-1]
        item["Name"] = response.xpath('//p[@class="detail_app_title"]/text()').extract_first()
        item["Version"] = response.xpath('//p[@class="detail_app_title"]/span/text()').extract_first().strip()
        item["Updated"] = response.xpath(
            '//p[contains(text(),"详细信息")]/following-sibling::p[1]/text()[2]').extract_first().strip()[5:]
        item["Developer"] = response.xpath(
            '//p[contains(text(),"详细信息")]/following-sibling::p[1]/text()[4]').extract_first().strip()[6:]
        item["headers"] = b";".join(response.headers.getlist("Set-Cookie")).decode('utf-8')
        item["categories"] = category
        # item["file_urls"] = [response.xpath('/html/body/script[1]/text()').extract_first().split('"')[1]]
        item["file_urls"] = response.xpath('/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/a[1]/@href').extract()
        item["app_url"] = response.request.url
        item["crawled_time"] = time.asctime(time.localtime(time.time()))
        item["file_type"] = '.apk'
        item["installs"] = response.xpath('/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/p[2]/text()').extract_first().split('/')[1].strip()
        yield item
