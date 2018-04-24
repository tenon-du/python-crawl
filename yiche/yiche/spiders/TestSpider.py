# coding=utf-8

import scrapy

from yiche.items import SerialItem


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = 'car.bitauto.com/tree_chexing/'
    start_urls = ['http://car.bitauto.com/tree_chexing/mb_196/']

    def parse(self, response):
        print '==> %s' % response.url
        # 品牌下的全部车系及车型
        brands = response.xpath('//*[@id="divCsLevel_0"]/*')
        size = len(brands)
        if size % 2 == 0:
            for i in range(size / 2):
                vendor = brands[i * 2].xpath('a/text()')[0].re(r'(\w+)>>')[0]
                for serial in brands[i * 2 + 1].xpath('div'):
                    item = SerialItem()
                    item['name'] = serial.xpath('div/div/a/@title')[0].extract()
                    item['logo'] = serial.xpath('div/div/a/img/@src')[0].extract()
                    item['id'] = serial.xpath('div/div/a/@id')[0].re(r'n(\d+)')[0]
                    item['vendor'] = vendor
                    yield item
        else:
            for serial in brands.xpath('div'):
                item = SerialItem()
                item['name'] = serial.xpath('div/div/a/@title')[0].extract()
                item['logo'] = serial.xpath('div/div/a/img/@src')[0].extract()
                item['id'] = serial.xpath('div/div/a/@id')[0].re(r'n(\d+)')[0]
                # item['vendor'] = vendor
                yield item
            pass
