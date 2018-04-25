# coding=utf-8
import json

import scrapy

from yiche.items import ModelItem


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = 'http://car.bitauto.com'
    start_urls = ['http://car.bitauto.com/AjaxNew/GetNoSaleSerailListByYear.ashx?csID=%s&year=%s' % ('3887', '2007')]

    def parse(self, response):
        print '==> %s' % response.url
        sid = response.meta['sid']
        try:
            datas = json.loads(response.body_as_unicode())
            for data in datas:
                classify = data['Engine_Exhaust'] + '/' + data['MaxPower'] + ' ' + data['InhaleType']
                for car in data['carList']:
                    item = ModelItem()
                    item['id'] = car['CarID']
                    item['sid'] = sid
                    item['name'] = car['YearType'] + ' ' + car['Name']
                    item['classify'] = classify
                    item['sell'] = '0'
                    yield item
        except ValueError:
            pass
