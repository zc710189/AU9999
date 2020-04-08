# -- coding: utf-8 --
import scrapy
from ..items import BaiduInformationItem


class BaiduInformationSpider(scrapy.Spider):
    name = 'baiduInformation'
    allowed_domains = ['www.baidu.com']
    start_url = ['https://www.baidu.com/']

    def parse(self, response):
        print('网页：', response.url)



