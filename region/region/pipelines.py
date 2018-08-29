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


# 解析品牌入库
class MySqlPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            db='test',
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
        n = tb.execute('select * from region where adCode = %s ', (item["adCode"],))
        if n == 1:
            tb.execute('update region set name = %s,py = %s,initial = %s,level = %s,parent = %s where adCode = %s',
                       (item["name"], item["py"], item["initial"], item["level"], item["parent"], item["adCode"]))
        else:
            tb.execute('insert into region(adCode,name,py,initial,level,parent) values(%s,%s,%s,%s,%s,%s)',
                       (item["adCode"], item["name"], item["py"], item["initial"], item["level"], item["parent"]))

    # 错误处理方法
    @staticmethod
    def handle_error(failue):
        print('--------------database operation exception!!-----------------')
        print(failue)
