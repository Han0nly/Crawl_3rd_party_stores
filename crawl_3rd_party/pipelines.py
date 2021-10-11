# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import FilesPipeline
from scrapy.exceptions import DropItem
from crawl_3rd_party.settings import ua

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
        if (item['ID'].startswith('Apkpure_') or item['ID'].startswith('Wandoujia_')):
            for i in range(0, len(item.get(self.files_urls_field, []))):
                if '.apk' == item.get("file_type", []):
                    meta = {'filename': item['ID'] + "_" + item.get("Version", [])[i] + '.apk'}
                else:
                    meta = {'filename': item['ID'] + "_" + item.get("Version", [])[i] + item.get("file_type", [])[i]}
                yield scrapy.Request(item.get(self.files_urls_field, [])[i], meta=meta, headers={"Cookie": headers, "USER_AGENT": ua})
        # elif (item['ID'].startswith('360_')):
        #     meta = {'filename': item['ID'] + '.apk'}
        #     for x in item.get(self.files_urls_field, []):
        #         yield scrapy.Request(x, meta=meta, headers={"Cookie": "__guid=170536683.3233737384537287000.1633956014089.3142", "USER_AGENT": ua})
        else:
            meta = {'filename': item['ID'] + '.apk'}
            for x in item.get(self.files_urls_field, []):
                yield scrapy.Request(x, meta=meta, headers={"Cookie": headers, "USER_AGENT": ua})

    def file_path(self, request, response=None, info=None, *, item=None):
        return "%s/%s" % (request.meta.get('categories', ''), request.meta.get('filename', ''))
