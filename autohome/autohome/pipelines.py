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


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('model.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_close(self, spider):
        self.file.close()


# 解析品牌入库
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


# 解析车系入库
class MySqlSeiralPipeline(object):
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
        n = tb.execute('select * from car_serial where id = %s ', (item["id"],))
        if n == 1:
            tb.execute('update car_serial set bid = %s ,name = %s ,vendor = %s ,date = %s where id = %s',
                       (item["bid"], item["name"], item["vendor"], item["date"], item["id"]))
        else:
            tb.execute('insert into car_serial(id,bid,name,vendor,date) values(%s,%s,%s,%s,%s)',
                       (item["id"], item["bid"], item["name"], item["vendor"], item["date"]))

    # 错误处理方法
    @staticmethod
    def handle_error(failue):
        print('--------------database operation exception!!-----------------')
        print(failue)


# 解析车型入库
class MySqlModelPipeline(object):
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
        n = tb.execute('select * from car_model where id = %s ', (item["id"],))
        if n == 1:
            tb.execute('update car_model set sid = %s ,name = %s ,classify = %s ,selling = %s ,date = %s where id = %s',
                       (item["sid"], item["name"], item["classify"], item["selling"], item["date"], item["id"]))
        else:
            tb.execute('insert into car_model(id,sid,name,classify,selling,date) values (%s,%s,%s,%s,%s,%s)',
                       (item["id"], item["sid"], item["name"], item["classify"], item["selling"], item["date"]))

    # 错误处理方法
    @staticmethod
    def handle_error(failue):
        print('--------------database operation exception!!-----------------')
        print(failue)
