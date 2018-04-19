# coding=utf-8

import scrapy
import time
from autohome.items import BrandItem


class BrandSpider(scrapy.Spider):
    name = "brand"
    allowed_domains = 'autohome.com.cn'
    # start_urls = ['https://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    # 测试地址
    start_urls = ['https://www.autohome.com.cn/grade/carhtml/A.html']

    def parse(self, response):
        print ("===> " + response.url)
        for brands in response.xpath('body/dl'):
            item = BrandItem()
            item['id'] = brands.xpath('@id')[0].extract()
            item['name'] = brands.xpath('dt/div/a/text()')[0].extract()
            item['logo'] = 'https:' + brands.xpath('dt/a/img/@src')[0].extract()
            item['initial'] = response.url[42:43]
            item['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            yield item
