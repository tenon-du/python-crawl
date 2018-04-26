# coding=utf-8
import json
import re

import scrapy
from scrapy.spiders import Rule

from scrapy.linkextractors import LinkExtractor
from yiche.items import BrandItem, SerialItem, ModelItem


# json替换key
def replacea(matched):
    return '\"' + matched.group('value') + '\":'


# 解析车系Item
def parse_serial_item(serial, bid, vendor):
    item = SerialItem()
    item['id'] = serial.xpath('div/div/a/@id')[0].re(r'n(\d+)')[0]
    item['bid'] = bid
    item['name'] = serial.xpath('div/div/a/@title')[0].extract()
    item['vendor'] = vendor
    item['logo'] = serial.xpath('div/div/a/img/@src')[0].extract()
    sell = serial.xpath('div/ul/li[@class="price"]/a/text()')[0].re(ur'停售')
    item['sell'] = '0' if sell else '1'
    return item


class YiCheSpider(scrapy.Spider):
    name = "yiche"

    rules = (
        # 所有车系
        Rule(LinkExtractor(allow=(r'http://car\.bitauto\.com/tree_chexing/mb_\d+/$',)), callback='parse_serial', follow=True),
        # 所有车型
        Rule(LinkExtractor(allow=(r'http://car\.bitauto\.com/tree_chexing/sb_\d+/$',)), callback='page_to_model', follow=True),
        # 在售车型
        Rule(LinkExtractor(allow=(r'http://car\.bitauto\.com/\w+/$',)), callback='parse_model', follow=True),
        # 停售车型
        Rule(LinkExtractor(allow=(r'http://car\.bitauto\.com/AjaxNew/GetNoSaleSerailListByYear\.ashx?csID=\d+&year=\d+$',)),
             callback='parse_model_selled', follow=True),
    )

    def start_requests(self):
        url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print '==> %s' % response.url

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
                    request = scrapy.Request(url, callback=self.parse_serial, dont_filter=True)
                    request.meta['bid'] = item['id']
                    yield request
            except KeyError:
                pass

        # url = 'http://car.bitauto.com/tree_chexing/mb_%s/' % '2'
        # request = scrapy.Request(url, callback=self.parse_serial, dont_filter=True)
        # request.meta['bid'] = '2'
        # yield request

    def parse_serial(self, response):
        print '==> %s' % response.url

        bid = response.meta['bid']
        # 品牌下的全部车系及车型
        brands = response.xpath('//*[@id="divCsLevel_0"]/*')
        size = len(brands)
        if size % 2 == 0:
            for i in range(size / 2):
                vendor = brands[i * 2].xpath('a/text()')[0].re(r'(\w+)>>')[0]
                for serial in brands[i * 2 + 1].xpath('div'):
                    item = parse_serial_item(serial, bid, vendor)
                    yield item

                    url = 'http://car.bitauto.com/tree_chexing/sb_%s/' % item['id']
                    request = scrapy.Request(url, callback=self.page_to_model, dont_filter=True)
                    request.meta['sid'] = item['id']
                    yield request
        else:
            for serial in brands.xpath('div'):
                item = parse_serial_item(serial, bid, '')
                yield item

                url = 'http://car.bitauto.com/tree_chexing/sb__%s/' % item['id']
                request = scrapy.Request(url, callback=self.page_to_model, dont_filter=True)
                request.meta['sid'] = item['id']
                yield request

        # url = 'http://car.bitauto.com/tree_chexing/sb_%s/' % '3887'
        # request = scrapy.Request(url, callback=self.page_to_model, dont_filter=True)
        # request.meta['sid'] = '3887'
        # yield request

    def page_to_model(self, response):
        print '==> %s' % response.url

        url = 'http://car.bitauto.com%s' % response.xpath('//div[@class="more"]/a[1]/@href')[0].extract()
        request = scrapy.Request(url, callback=self.parse_model, dont_filter=True)
        request.meta['sid'] = response.meta['sid']
        yield request

    def parse_model(self, response):
        print '==> %s' % response.url

        sid = response.meta['sid']
        # 在售车型
        classify = ''
        for tr in response.xpath('//*[@id="compare_sale"]/tbody/*'):
            try:
                th = tr.xpath('th[1]/text()')[1].extract().rstrip()
                strong = tr.xpath('th[1]/strong/text()')[0].extract()
                classify = strong + '/' + th
            except IndexError:
                item = ModelItem()
                item['id'] = tr.xpath('td[1]/a[1]/@href')[0].re(r'/m(\d+)/')[0]
                item['sid'] = sid
                item['name'] = tr.xpath('td[1]/a[1]/text()')[0].extract()
                item['classify'] = classify
                item['sell'] = '1'
                yield item

        # 停售车型
        years = response.xpath('//*[@id="carlist_nosaleyear"]/a/@id').extract()
        for year in years:
            url = 'http://car.bitauto.com/AjaxNew/GetNoSaleSerailListByYear.ashx?csID=%s&year=%s' % (sid, year)
            request = scrapy.Request(url=url, callback=self.parse_model_selled, dont_filter=True)
            request.meta['sid'] = sid
            yield request

    @staticmethod
    def parse_model_selled(response):
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
            print 'model parse error,serial_id[%s].' % sid
            pass
