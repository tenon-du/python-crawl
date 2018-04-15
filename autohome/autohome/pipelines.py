# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class JsonWithEncodingBrandPipeline(object):
    def __init__(self):
        self.file = codecs.open('brand.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_close(self, spider):
        self.file.close()


class MySqlBrandPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db='drive_collect',
            user='root',
            passwd='',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=False)

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    # 写入数据库中
    @staticmethod
    def _conditional_insert(tb, item):
        n = tb.execute('select * from car_brand where id = %s ', (item["id"],))
        if n == 1:
            tb.execute('update car_brand set name = %s , logo = %s ,initial = %s ,date = %s where id = %s',
                       (item["name"], item["logo"], item["initial"], item["date"], item["id"]))
        else:
            tb.execute('insert into car_brand(id,name,logo,initial,date) values(%s,%s,%s,%s,%s)',
                       (item["id"], item["name"], item["logo"], item["initial"], item["date"]))

    # 错误处理方法
    @staticmethod
    def handle_error(failue):
        print('--------------database operation exception!!-----------------')
        print(failue)
