# coding=utf-8

import scrapy
import time
from autohome.items import SerialItem


class BrandSpider(scrapy.Spider):
    name = "serial"
    allowed_domains = 'autohome.com.cn'
    start_urls = ['https://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    # 测试地址
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/D.html']

    def parse(self, response):
        print ("===> " + response.url)
        for brand in response.xpath('body/dl'):
            vendors = brand.xpath('dd/div/text()')
            size = len(vendors)
            for i in range(0, size):
                for serial in brand.xpath('dd/ul[%d]/li' % (i + 1)):
                    try:
                        item = SerialItem()
                        item['bid'] = brand.xpath('@id')[0].extract()
                        item['vendor'] = vendors[i].extract()
                        item['id'] = serial.xpath('@id')[0].extract()[1:]
                        item['name'] = serial.xpath('h4/a/text()')[0].extract()
                        item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        yield item
                    except IndexError:
                        pass
