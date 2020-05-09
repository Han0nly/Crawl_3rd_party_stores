# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import FilesPipeline
from scrapy.exceptions import DropItem


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class Crawl3RdPartyPipeline:
    def process_item(self, item, spider):
        return item


class MyFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        headers = item['headers']
        req_list = []
        if (item['ID'].startwith('Apkpure_')):
            for i in range(0, len(item.get(self.files_urls_field, []))):
                meta = {'filename': item['ID'] + "_" + item.get("Version", [])[i]}
                req_list.append(
                    scrapy.Request(item.get(self.files_urls_field, [])[i], meta=meta, headers={"Cookie": headers}))
        else:
            meta = {'filename': item['ID']}
            for x in item.get(self.files_urls_field, []):
                req_list.append(scrapy.Request(x, meta=meta, headers={"Cookie": headers}))
        return req_list

    # def get_media_requests(self, item, info):
    #     file_url = item['file_url']
    #     meta = {'filename': item['name']}
    #     yield scrapy.Request(url=file_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')
