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


class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_close(self, spider):
        self.file.close()


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

        n = tb.execute('select * from oil_price where area = %s ', (item["area"],))
        if n == 1:
            tb.execute('update oil_price set _89 = %s , _92 = %s ,_95 = %s ,_0 = %s ,update_time = %s where area = %s',
                       (item["_89"], item["_92"], item["_95"], item["_0"], item['update_time'], item["area"]))
        else:
            tb.execute('insert into oil_price(area,_89,_92,_95,_0,update_time) values(%s,%s,%s,%s,%s,%s)',
                       (item["area"], item["_89"], item["_92"], item["_95"], item["_0"], item['update_time']))

    # 错误处理方法
    @staticmethod
    def handle_error(failue):
        print('--------------database operation exception!!-----------------')
        print(failue)
