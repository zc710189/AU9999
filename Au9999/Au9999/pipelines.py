# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import hashlib
import pymysql as pm
from scrapy.exceptions import DropItem

def str_md5(str):
    return hashlib.md5(str.encode()).hexdigest()

def write_date_json(item, filePath):
    with open(filePath, 'w') as fJson:
        json.dump(dict(item), fJson)
        fJson.close()

def write_date_mysql(item, content_path):
    database = pm.connect("localhost", "root", "123456", "au9999")
    cursor = database.cursor()
    temp_item = dict(item)
    del (temp_item['content'])
    temp_item['content_path'] = content_path
    keys, values = '', ''
    for key in temp_item:
        keys += "%s," % key
        values += "'%s'," % temp_item[key]
    keys = keys.strip(',')
    values = values.strip(',')
    select_sql = "INSERT INTO information(%s) VALUES(%s);" % (keys, values)
    cursor.execute(select_sql)
    database.commit()
    cursor.close()
    database.close()


class Au9999Pipeline(object):
    def __init__(self):
        self.filePath = r'C:/Users/CZ/PycharmProjects/AU9999/Au9999/Au9999/information'
        self.urlsPath = r'C:/Users/CZ/PycharmProjects/AU9999/Au9999/Au9999/information/url'
        self.urls = []

    def process_item(self, item, spider):
        urlsPath = '%s/%s' % (self.urlsPath, spider.allowed_domains[0])
        if not os.path.exists(urlsPath):
            os.makedirs(urlsPath)
            f = open('%s/url.txt' % urlsPath, 'w')
            f.close()
        with open('%s/url.txt' % urlsPath, 'r') as f:
            for line in f.readlines():
                self.urls.append(line.strip())
            f.close()
        if item['url'] not in self.urls:
            filePath = '%s/%s/%s' % (self.filePath, spider.name, item['publish_time'])
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            write_date_json(item, '%s/%s.json' % (filePath, str_md5(item['url'])))
            write_date_mysql(item, '%s/%s.json' % (filePath, str_md5(item['url'])))
            with open('%s/url.txt' % urlsPath, 'a') as f:
                f.write(item['url']+'\n')
                f.close()
            return item
        else:
            raise DropItem("Duplicate found")

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

