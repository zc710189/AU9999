# -- coding: utf-8 --
import scrapy
from ..items import InformationItem
from scrapy.http import Request
import time

class dyhjwSpider(scrapy.Spider):
    name = 'dyhjw'
    allowed_domains = ['www.dyhjw.com']
    start_urls = ['http://www.dyhjw.com/gold/jjsj.html']
    custom_settings = {
        'ITEM_PIPELINES': {'Au9999.pipelines.Au9999Pipeline': 1}
    }

    def parse(self, response):
        domain = 'http://www.dyhjw.com/'
        blog_urls = response.xpath("//div[@class='news_list_pic']/a/@href").extract()
        if not blog_urls:
            return
        for blog_url in blog_urls[:2]:
            blog_url = domain + blog_url if domain not in blog_url else blog_url
            yield Request(url=blog_url, callback=self.contentParse)
        next_url = response.xpath("//a[@class='next']/@href").extract_first()
        if next_url:
            pass
            #yield Request(url=next_url, callback=self.parse)

    def contentParse(self, response):
        item = InformationItem()
        item['url'] = response.url
        item['title'] = None
        item['publish_time'] = None
        item['publisher'] = None
        item['crawl_time'] = time.strftime("%Y-%m-%d")
        item['content'] = None

        title = response.xpath("//h1/text()").extract_first()
        item['title'] = title if title else None

        publish_time = response.xpath("//span[@id='pushtime']/text()").extract_first()
        if u'\u5c0f\u65f6\u524d' in publish_time or u'\u5206\u949f\u524d' in publish_time:
            publish_time = time.strftime("%Y-%m-%d")
        else:
            publish_time = publish_time.split(' ')[0].replace(u'\u5e74', '-').replace(u'\u6708', '-').replace(u'\u65e5', '').strip()
        item['publish_time'] = publish_time if publish_time else None

        publisher = response.xpath("//div[@class='zrbj']/text()").extract_first()
        publisher = publisher.replace(u'\u8d23\u4efb\u7f16\u8f91\uff1a', '').strip()
        item['publisher'] = publisher if publisher else None

        content = ''.join(response.xpath("//div[@class='section_wrap']//text()").extract())
        item['content'] = content if content else None

        yield item









