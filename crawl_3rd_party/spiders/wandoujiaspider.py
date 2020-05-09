# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawl_3rd_party.items import Crawl3RdPartyItem
from scrapy.selector import Selector
import requests

class WandoujiaspiderSpider(CrawlSpider):
    name = 'wandoujiaspider'
    allowed_domains = ['wandoujia.com']
    start_urls = []
    for i in range(1,42):
        start_urls.append('https://www.wandoujia.com/wdjweb/api/category/more?catId=5028&subCatId=647&page='+str(i))

    rules = (
        Rule(LinkExtractor(allow=(r'https://www.wandoujia.com/wdjweb/api/category/more', )), follow=False, callback='parse_link'),
    )
    def parse_start_url(self, response):
        return self.parse_link(response)

    def parse_link(self,response):
        if(json.loads(response.text)["state"]["msg"]!="Ok"):
            yield response.request
        elif(json.loads(response.text)["data"]["currPage"]):
            content = json.loads(response.text)["data"]["content"]
            urls = Selector(text=content).xpath("/li/div[1]/a[1]/@href").extract()
            for url in urls:
                yield scrapy.Request(url=url+"/history",callback=self.parse_versions)
            # content.xpath("")

    def parse_versions(self, response):
        # for title in response.xpath('/html'):
        item = Crawl3RdPartyItem()
        item["ID"] = "Wandoujia_"+response.xpath('/html/body/@data-pn').extract_first()
        item["Name"] = response.xpath('/html/body/@data-title').extract_first()
        item["Developer"] = []
        item["Version"] = []
        item["Updated"] = []
        item["headers"] = []
        item["file_urls"] = []
        version_links = response.xpath('//ul[@class="old-version-list"]/li/a[1]/@href').extract()
        for version_link in version_links:
            r = requests.get(version_link)
            item["Version"].append(Selector(text=r.text).xpath('//a[@class="install-btn i-source "]/@data-app-vname').extract_first())
            if version_link.count('/'):
                item["Updated"].append(
                    Selector(text=r.text).xpath('//span[@class="update-time"]/@datetime').extract_first())
            item["headers"].append(";".join(r.headers.get("Set-Cookie")))
            item["file_urls"].append(Selector(text=r.text).xpath('//a[@class="normal-dl-btn "]li/@href').extract_first())
            if not item["Developer"]:
                item["Developer"] = Selector(text=r.text).xpath("/li/div[1]/a[1]/@href").extract_first()
        yield item
