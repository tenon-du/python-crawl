# coding=utf-8

import scrapy
import time
from autohome.items import SeriesItem


class BrandSpider(scrapy.Spider):
    name = "serial"
    allowed_domains = 'autohome.com.cn'
    url = 'https://www.autohome.com.cn/grade/carhtml/%s.html'

    start_urls = ['https://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    # 测试地址
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/A.html']

    def parse(self, response):
        print("===>", response.url)
        for brands in response.xpath('body/dl'):
            serials = brands.xpath('dd/ul/li')
            for serial in serials:
                try:
                    item = SeriesItem()
                    item['bid'] = brands.xpath('@id')[0].extract()
                    item['vendor'] = brands.xpath('dd/div/text()')[0].extract()
                    item['id'] = serial.xpath('@id')[0].extract()[1:]
                    item['name'] = serial.xpath('h4/a/text()')[0].extract()
                    item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                    yield item
                except IndexError:
                    pass
