# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Au9999Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BaiduInformationItem(scrapy.Item):
    title = scrapy.Field()
    domain = scrapy.Field()
    publish_time = scrapy.Field()
    crawl_time = scrapy.Field()
    content = scrapy.Field()



