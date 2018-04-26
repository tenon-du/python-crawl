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

from yiche.items import BrandItem, SerialItem, ModelItem


class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_close(self, spider):
        self.file.close()


# 解析品牌入库
class MySqlPipeline(object):
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
        # 品牌
        if isinstance(item, BrandItem):
            n = tb.execute('select * from car_brand where id = %s ', (item["id"],))
            if n == 1:
                tb.execute('update car_brand set name = %s , logo = %s ,initial = %s where id = %s',
                           (item["name"], item["logo"], item["initial"], item["id"]))
            else:
                tb.execute('insert into car_brand(id,name,logo,initial) values(%s,%s,%s,%s)',
                           (item["id"], item["name"], item["logo"], item["initial"]))
        # 车系
        elif isinstance(item, SerialItem):
            n = tb.execute('select * from car_serial where id = %s ', (item["id"],))
            if n == 1:
                tb.execute('update car_serial set bid = %s ,name = %s ,vendor = %s ,logo = %s ,sell = %s  where id = %s',
                           (item["bid"], item["name"], item["vendor"], item["logo"], item["sell"], item["id"]))
            else:
                tb.execute('insert into car_serial(id,bid,name,vendor,logo,sell) values(%s,%s,%s,%s,%s,%s)',
                           (item["id"], item["bid"], item["name"], item["vendor"], item["logo"], item["sell"]))
        # 车型
        elif isinstance(item, ModelItem):
            n = tb.execute('select * from car_model where id = %s ', (item["id"],))
            if n == 1:
                tb.execute('update car_model set sid = %s ,name = %s ,classify = %s ,sell = %s  where id = %s',
                           (item["sid"], item["name"], item["classify"], item["sell"], item["id"]))
            else:
                tb.execute('insert into car_model(id,sid,name,classify,sell) values (%s,%s,%s,%s,%s)',
                           (item["id"], item["sid"], item["name"], item["classify"], item["sell"]))
        else:
            pass

    # 错误处理方法
    @staticmethod
    def handle_error(failue):
        print('--------------database operation exception!!-----------------')
        print(failue)
