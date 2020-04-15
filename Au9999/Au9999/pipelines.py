# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import hashlib
import pymysql as pm

def str_md5(str):
    return hashlib.md5(str.encode()).hexdigest()

def write_date_json(item, filePath):
    with open(filePath + '/' + str_md5(item['url']) + '.json', 'w') as fJson:
        json.dump(dict(item), fJson)
        fJson.close()

def write_date_mysql(item, content_path):
    database = pm.connect("localhost", "root", "123456", "au9999")
    cursor = database.cursor()
    temp_item = item
    del (temp_item['content'])
    temp_item['content_path'] = content_path + '/' + str_md5(item['url']) + '.json'
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
        self.filePath = './information/'

    def process_item(self, item, spider):
        print('***************')
        write_date_json(item, self.filePath)
        write_date_mysql(item, self.filePath)
        print('***************')
        return item

    def open_spider(self, spider):
        self.filePath += spider.name
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

    def close_spider(self, spider):
        pass

