# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawl3RdPartyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    Name = scrapy.Field()
    Version = scrapy.Field()
    Updated = scrapy.Field()
    Developer = scrapy.Field()
    headers = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_type = scrapy.Field()
    categories = scrapy.Field()
    installs = scrapy.Field()
    crawled_time = scrapy.Field()
    app_url = scrapy.Field()
