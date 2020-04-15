# -- coding: utf-8 --
import scrapy
from ..items import InformationItem
from scrapy.http import Request
import time

class informationSpider(scrapy.Spider):
    name = 'information'
    allowed_domains = ['www.dyhjw.com']
    start_urls = ['http://www.dyhjw.com/gold/jjsj.html']

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

        # if u'小时前' in publish_time:
        #     publish_time = time.strftime("%Y-%m-%d")
        # else:
        #     publish_time = publish_time.split(' ')[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '').strip()
        item['publish_time'] = publish_time if publish_time else None

        publisher = response.xpath("//div[@class='zrbj']/text()").extract_first()
        # publisher = publisher.replace(u'责任编辑：').strip()
        item['publisher'] = publisher if publisher else None

        content = ''.join(response.xpath("//div[@class='section_wrap']//text()").extract())
        item['content'] = content if content else None

        yield item









