# coding=utf-8
import json
import re

import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule

from yiche.items import BrandItem


def replacea(matched):
    return '\"' + matched.group('value') + '\":'


class YiCheSpider(scrapy.Spider):
    name = "yiche"

    rules = (
        # 字母分区页
        Rule(SgmlLinkExtractor(allow=(r'http://car\.bitauto\.com/tree_chexing/mb_\d+/',)), callback='parse_serial', follow=True),
    )

    def start_requests(self):
        url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        result = re.sub('(?P<value>\w+):', replacea, response.text[response.text.find('{'):response.text.rfind('}') + 1])
        data = json.loads(result)

        for char in data['char']:
            print '==> %s' % char
            try:
                for brand in data['brand']['%s' % char]:
                    item = BrandItem()
                    item['id'] = brand['id']
                    item['name'] = brand['name']
                    item['logo'] = 'http://image.bitautoimg.com/bt/car/default/images/logo/masterbrand/png/100/m_%s_100.png' % item['id']
                    item['initial'] = char
                    yield item

                    url = 'http://car.bitauto.com/tree_chexing/mb_%s/' % item['id']
                    yield scrapy.Request(url, callback=self.parse_serial, dont_filter=True)
            except KeyError:
                pass

    def parse_serial(self, response):
        print '==> %s' % response.url
